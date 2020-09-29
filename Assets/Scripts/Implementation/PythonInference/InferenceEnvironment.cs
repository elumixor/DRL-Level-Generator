using System.Linq;
using DRL.Behaviours;
using Implementation.Dummy;
using NaughtyAttributes;
using Player;
using UnityEngine;

namespace Implementation.PythonInference {
    public class InferenceEnvironment : Environment<DummyAction, Observation> {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        public override void ResetEnvironment() {
            player.ResetState();
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
        }

        public override (float reward, bool isDone) Step(DummyAction action) {
            if (action.tap) playerInputHandler.OnTap();

            return (1f, false);
        }

        protected override Observation CurrentObservation {
            get {
                var playerPosition = GameObject.FindWithTag("Player").transform.position.x;
                var enemiesPositions = FindObjectsOfType<Enemy>().Select(e => (Vector2) e.transform.position).ToArray();

                return new Observation {enemiesPositions = enemiesPositions, playerPosition = playerPosition};
            }
        }
    }
}