using System.Linq;
using Common;
using DRL.Behaviours;
using NaughtyAttributes;
using Player;
using UnityEngine;

namespace Implementation.Dummy {
    public class DummyEnvironment : Environment<DummyAction, DummyObservation> {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        public override void ResetEnvironment() {
            player.ResetState();
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
        }

        public override (float reward, bool isDone) Step(DummyAction action) {
            if (action.tap) {
                playerInputHandler.OnTap();
            }

            return (1f, false);
        }

        protected override DummyObservation CurrentState {
            get {
                return new DummyObservation {distanceToClosest = 0f};
            }
        }
    }
}