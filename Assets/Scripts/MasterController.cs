using System.Linq;
using BackendCommunication;
using Common;
using Configuration;
using DRL;
using DRL.Behaviours;
using Serialization;
using UnityEngine;

/// <summary>
///     Reads and stores global training configurations (<see cref="TrainingSetupConfiguration" />)
///     Should be unique per every training setup
/// </summary>
public class MasterController<TAction, TState> : SingletonBehaviour<MasterController<TAction, TState>> {
    const string TPP_ADDRESS = "tcp://localhost:5555";

    [SerializeField] TrainingSetupConfiguration trainingSetupConfiguration;
    static TrainingSetupConfiguration TrainingSetupConfiguration => instance.trainingSetupConfiguration;

    /// <summary>
    ///     The main entry point for each Training Setup
    /// </summary>
    /// Initializes NNs in all the agents in the scene
    /// Initializes serializers, given the state size and action size
    /// Sends initial data via communicator to initialize backend
    void Start() {
        var actionSize = StructuralAttribute.GetSize(typeof(TAction));
        var stateSize = StructuralAttribute.GetSize(typeof(TState));

        foreach (var nnAgent in FindObjectsOfType<Agent<TAction, TState>>().OfType<INNAgent>())
            nnAgent.InitializeNN(TrainingSetupConfiguration.AlgorithmConfiguration.ActorLayout);

        Communicator.OpenConnection(TPP_ADDRESS);

        // TODO
        // var message = new { };
        // var response = Communicator.SendMessage(message);
    }

    void OnDestroy() { Communicator.CloseConnection(); }
}