using System;
using UnityEngine;

namespace Common
{
    [Serializable]
    public class Circle
    {
        public float radius = 1;
        public Vector2 position;

        public Circle(Vector2 position, float radius)
        {
            this.position = position;
            this.radius   = radius;
        }

        public bool Intersects(Circle other) => (position - other.position).magnitude - radius - other.radius <= 0;
    }
}
