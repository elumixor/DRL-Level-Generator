namespace RemoteComputation.Models
{
    public interface IRemoteModel
    {
        int Id { get; }
        ModelType ModelType { get; }
    }
}
