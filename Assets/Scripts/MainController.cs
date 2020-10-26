using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using BackendCommunication;
using Common;
using Common.ByteConversions;
using Configuration;
using DRL;
using DRL.Behaviours;
using NN;
using Serialization;
using UnityEditor;
using UnityEngine;
using Debug = UnityEngine.Debug;

/// <summary>
///     Reads and stores global training configurations (<see cref="TrainingSetupConfiguration" />)
///     Should be unique per every training setup
/// </summary>
public class MasterController<TAction, TState, TEnvironment, TAgent> : SingletonBehaviour<
    MasterController<TAction, TState, TEnvironment, TAgent>>
    where TEnvironment : Environment<TAction, TState> where TAgent : Agent<TAction, TState> {
    const string SERVER_MAIN_PATH = "src/main.py";
    const string TCP_ADDRESS = "tcp://localhost:5555";
    const string TCP_ADDRESS_SERVER = "tcp://*:5555";

    [SerializeField] Trainer<TAction, TState, TEnvironment, TAgent> trainer;
    [SerializeField] TrainingSetupConfiguration trainingSetupConfiguration;

    Process serverProcess;

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

            // Start training
            trainer.StartTraining();
            trainer.trainer.TrainingFinished += () => EditorApplication.isPlaying = false;
        } catch (CommunicationException e) {
            Debug.LogException(e);
            EditorApplication.isPlaying = false;
        }
    }

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