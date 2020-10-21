﻿using System.Collections;
using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using DRL;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class Transition : IEnumerable<float> {
        public readonly Action action;
        public readonly State previousState;
        public readonly float reward;
        public readonly State nextState;

        public Transition(State previousState, Action action, float reward, State nextState) {
            this.previousState = previousState;
            this.action = action;
            this.reward = reward;
            this.nextState = nextState;
        }

        public IEnumerator<float> GetEnumerator() {
            foreach (var f in previousState) yield return f;
            yield return action.FloatValue;
            yield return reward;
            foreach (var f in nextState) yield return f;
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}