using System;
using NaughtyAttributes;
using UnityEngine;

namespace Common
{
    public class FollowTransform : MonoBehaviour
    {
        [Flags]
        public enum LockPosition
        {
            None = 0,
            X = 1,
            Y = 2,
            Z = 4,
        }

        public float followStrength;

        [EnumFlags] public LockPosition lockPosition;
        public Vector3 offset;

        public Transform toFollow;

        void Update()
        {
            var p = transform.position;
            var pp = toFollow.position + offset;

            var interpolated = Vector3.Lerp(p, pp, followStrength * Time.unscaledDeltaTime);

            if ((lockPosition & LockPosition.X) == LockPosition.X) interpolated.x = p.x;
            if ((lockPosition & LockPosition.Y) == LockPosition.Y) interpolated.y = p.y;
            if ((lockPosition & LockPosition.Z) == LockPosition.Z) interpolated.z = p.z;

            transform.position = interpolated;
        }

        [Button]
        public void Synchronize()
        {
            var p = transform.position;
            var pp = toFollow.position + offset;

            if ((lockPosition & LockPosition.X) == LockPosition.X) pp.x = p.x;
            if ((lockPosition & LockPosition.Y) == LockPosition.Y) pp.y = p.y;
            if ((lockPosition & LockPosition.Z) == LockPosition.Z) pp.z = p.z;

            transform.position = pp;
        }
    }
}
