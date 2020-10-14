using Common;
using NaughtyAttributes;
using UnityEngine;

namespace Configuration {
    /// <summary>
    /// Reads and stores global training configurations (<see cref="Configuration"/>)
    /// </summary>
    public class MasterController : SingletonBehaviour<MasterController> {
        [SerializeField, Expandable] Configuration configuration;
        
        
    }
}