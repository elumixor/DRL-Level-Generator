using System.Linq;
using BackendCommunication;
using Common;
using Configuration;
using DRL;
using DRL.Behaviours;
using NN;
using Serialization;
using UnityEditor;
using UnityEngine;

/// <summary>
///     Reads and stores global training configurations (<see cref="TrainingSetupConfiguration" />)
///     Should be unique per every training setup
/// </summary>
public class MasterController<TAction, TState> : SingletonBehaviour<MasterController<TAction, TState>> {
    const string TPP_ADDRESS = "tcp://localhost:5555";
    [SerializeField] DRL.Behaviours.Trainer<TAction, TState> trainer;

    [SerializeField] TrainingSetupConfiguration trainingSetupConfiguration;

    static TrainingSetupConfiguration TrainingSetupConfiguration => instance.trainingSetupConfiguration;

    /// <summary>
    ///     The main entry point for each Training Setup
    /// </summary>
    /// Initializes NNs in all the agents in the scene
    /// Initializes serializers, given the state size and action size
    /// Sends initial data via communicator to initialize backend
    void Start() {
        try {
            // Open connection and ping back end to see if it is responsive
            Communicator.OpenConnection(TPP_ADDRESS);
            Communicator.Send(RequestType.WakeUp);

            // If everything is ok, send initial configuration data
            var actionSize = StructuralAttribute.GetSize(typeof(TAction));
            var stateSize = StructuralAttribute.GetSize(typeof(TState));

            var configuration = TrainingSetupConfiguration;
            configuration.actionSize = actionSize;
            configuration.stateSize = stateSize;

            // Communicator should return the initial nn learnable parameters
            var (nnData, startIndex) = Communicator.Send(RequestType.SendConfiguration, configuration.ToBytes());
            var stateDict = new StateDict(nnData, startIndex);

            // Initialize agents with current parameters and configuration
            foreach (var nnAgent in FindObjectsOfType<Agent<TAction, TState>>().OfType<INNAgent>()) {
                nnAgent.InitializeNN(TrainingSetupConfiguration.AlgorithmConfiguration.ActorLayout);
                nnAgent.NN.LoadStateDict(stateDict);
            }

            // Start training
            trainer.StartTraining();
        } catch (CommunicationException e) {
            Debug.LogError(e.Message);
            EditorApplication.isPlaying = false;
        }
    }

    void OnDestroy() { Communicator.CloseConnection(); }
}