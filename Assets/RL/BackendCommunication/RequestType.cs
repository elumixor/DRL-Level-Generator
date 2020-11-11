namespace RL.BackendCommunication
{
    /// <summary> Requests types (headers), supported by communication protocol </summary>
    public enum RequestType
    {
        /// For testing purposes. Server respond with the same message as sent by client
        Echo,

        /// Sent when entering play mode in Unity. Backend will close whatever is running and will get ready for new training session
        WakeUp,

        /// If server is up and running, will send the global configuration for this training setup,
        /// including algorithms, NN layouts, hyperparameters, state size, action size.
        SendConfiguration,

        /// Sends training data and lets the backend perform training
        SendTrainingData,

        /// Tells backend to stop and shut server down
        ShutDown,

        /// Requests info about current training progress
        RequestInfo,

        /// Save current work
        SaveSession,

        /// Resume work
        LoadSession,
    }
}
