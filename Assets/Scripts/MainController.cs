using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using Configuration;
using NaughtyAttributes;
using NN;
using RL;
using RL.Behaviours;
using Serialization;
using UnityEditor;
using UnityEngine;
using Debug = UnityEngine.Debug;

/// <summary>
///     Reads and stores global training configurations (<see cref="TrainingSetupConfiguration" />)
///     Should be unique per every training setup
/// </summary>
public class MainController<TAction, TState, TEnvironment, TAgent> : SingletonBehaviour<
    MainController<TAction, TState, TEnvironment, TAgent>>
    where TEnvironment : Environment<TAction, TState> where TAgent : Agent<TAction, TState> {
    const string SERVER_MAIN_PATH = "src/main.py";
    const string TCP_ADDRESS = "tcp://localhost:5555";
    const string TCP_ADDRESS_SERVER = "tcp://*:5555";

    [BoxGroup("Configuration"), SerializeField] TrainingSetupConfiguration trainingSetupConfiguration;

    [BoxGroup("Environments"), SerializeField] protected TAgent agent;
    [BoxGroup("Environments"), SerializeField] protected TEnvironment environment;

    [BoxGroup("Epochs and Episode lengths"), SerializeField] bool trainUnlimited;

    [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1), HideIf("trainUnlimited")]
    int epochs;

    [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int episodesPerEpoch;
    [BoxGroup("Epochs and Episode lengths"), SerializeField, MinValue(1)] int maximumEpisodeLength;

    [BoxGroup("Training speed"), SerializeField, Range(0, 500)] float speed;

    // on every Update() adds `speed` to itself and performs trainer steps for the number of time, rounded down to the closes integer
    float elapsed;

    // flag if Update() should run
    bool isTraining;

    // Python backend process
    Process serverProcess;

    // Controls the general RL logic 
    Trainer<TAction, TState> trainer;

    static TrainingSetupConfiguration TrainingSetupConfiguration => instance.trainingSetupConfiguration;

    /// <summary>
    ///     The main entry point for each Training Setup
    /// </summary>
    /// Initializes NNs in all the agents in the scene
    /// Initializes serializers, given the state size and action size
    /// Sends initial data via communicator to initialize backend
    void Start() {
        // Launch backend server (use separate window to monitor stuff)
        serverProcess = ProcessRunner.CreateProcess(SERVER_MAIN_PATH, new Dictionary<string, string> {{"address", TCP_ADDRESS_SERVER}},
                                                    separateWindow: true);
        serverProcess.Start();

        try {
            // Open connection and ping back end to see if it is responsive
            Communicator.OpenConnection(TCP_ADDRESS);
            Communicator.Send(RequestType.WakeUp, timeout: -1);

            // If everything is ok, send initial configuration data
            var actionSize = StructuralAttribute.GetSize(typeof(TAction));
            var stateSize = StructuralAttribute.GetSize(typeof(TState));

            var configuration = TrainingSetupConfiguration;
            configuration.actionSize = actionSize;
            configuration.stateSize = stateSize;

            // Communicator should return the initial nn learnable parameters
            var (nnData, startIndex) = Communicator.Send(RequestType.SendConfiguration, configuration.ToBytes());
            var stateDict = nnData.Get<StateDict>(startIndex).result;

            Debug.Log($"Received state dict: {stateDict}");

            // Initialize agents with current parameters and configuration
            foreach (var nnAgent in FindObjectsOfType<Agent<TAction, TState>>().OfType<INNAgent>())
                nnAgent.InitializeNN(TrainingSetupConfiguration.AlgorithmConfiguration.ActorLayout, stateDict);

            // Create trainer and start training
            trainer = new Trainer<TAction, TState>(environment, agent, trainUnlimited ? -1 : epochs, episodesPerEpoch,
                                                   maximumEpisodeLength);
            trainer.StartTraining();
            trainer.TrainingFinished += () => {
                Debug.Log("Training finished!");
                EditorApplication.isPlaying = false;
            };
            isTraining = true;
        } catch (CommunicationException e) {
            Debug.LogException(e);
            EditorApplication.isPlaying = false;
        }
    }

    // Updates trainer given the speed
    void Update() {
        if (!isTraining) return;

        elapsed += speed;

        while (elapsed >= 1f) {
            trainer.Step();
            elapsed -= 1f;
        }
    }

    // Shuts down server and process when exiting
    void OnDestroy() {
        try {
            Communicator.Send(RequestType.ShutDown);
        } catch (Exception exception) {
            Debug.LogWarning(exception);
        }

        Communicator.CloseConnection();
        serverProcess.Close();
    }
}