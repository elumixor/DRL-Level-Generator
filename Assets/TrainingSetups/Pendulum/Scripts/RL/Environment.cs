using System.Linq;
using Common;
using NaughtyAttributes;
using RL;
using TrainingSetups.Pendulum.Scripts.Player;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.RL
{
    public class Environment : MonoBehaviour, IEnvironment<State, Action>
    {
        [SerializeField, Required] PlayerBehaviouralController player;
        [SerializeField, Required] PlayerInputHandler playerInputHandler;

        bool isDone;

        protected State CurrentState {
            get {
                var playerPosition = GameObject.FindWithTag("Player").transform.position.x;
                var enemiesPositions = FindObjectsOfType<Enemy>().Select(e => (Vector2) e.transform.position).ToArray();

                return new State(playerPosition, player.Angle, player.AngularSpeed, player.UpwardSpeed);
            }
        }

        void Start() => player.Collided += () => isDone = true;

        // protected override void Update() {
        // base.Update();

        // if (player.transform.position.y >= 9f) isDone = true;
        // }

        public State ResetEnvironment()
        {
            player.ResetState();
            isDone = false;
            foreach (var followTransform in FindObjectsOfType<FollowTransform>()) followTransform.Synchronize();
            return CurrentState;
        }

        public (State newState, float reward, bool isDone) Step(Action action)
        {
            if (action.tap) playerInputHandler.OnTap();

            return (CurrentState, 1f, isDone);
        }
    }
}
