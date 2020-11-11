using System;
using UnityEngine;
using Random = UnityEngine.Random;

namespace TrainingSetups.Pendulum.Scripts
{
    [Serializable]
    public class EnvironmentParameter
    {
        [SerializeField] bool isConstant = true;

        [SerializeField] float constantValue;

        [SerializeField] float rangeMin;
        [SerializeField] float rangeMax;

        public static implicit operator float(EnvironmentParameter parameter) =>
                parameter.isConstant ? parameter.constantValue : Random.Range(parameter.rangeMin, parameter.rangeMax);

        public float Max {
            get => isConstant ? constantValue : rangeMax;
            set {
                if (isConstant)
                    constantValue = value;
                else
                    rangeMax = value;
            }
        }

        public float Min {
            get => isConstant ? constantValue : rangeMin;
            set {
                if (isConstant)
                    constantValue = value;
                else
                    rangeMin = value;
            }
        }
    }
}
