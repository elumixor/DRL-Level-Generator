using System;
using System.Collections;
using UnityEngine;

namespace Player {
    /// <summary>
    /// Responsible for player movement and executing player actions
    /// </summary>
    [RequireComponent(typeof(PlayerConfigurator))]
    public class PlayerBehaviouralController : MonoBehaviour {
        public event Action OnCollided = delegate { };

        [SerializeField] Transform rotatingPart;

        float angle;

        [SerializeField] float maxAngle;
        [SerializeField] float swingSpeed;
        [SerializeField] float upwardSpeed;

        [SerializeField] float upwardSpeedBoostStrength;
        [SerializeField] float upwardSpeedBoostTime;

        [SerializeField] float swingBoostStrength;
        [SerializeField] float swingBoostTime;

        float t;
        float direction = 1;
        float boost;
        float swingBoost;

        IEnumerator currentUpwardSpeedBoostCoroutine;
        IEnumerator currentSwingBoostCoroutine;

        void Update() {
            t += Time.deltaTime * (swingSpeed + swingBoost) * direction;
            var a = Mathf.Sin(t) * maxAngle;

            rotatingPart.localEulerAngles = Vector3.forward * a;
            transform.localPosition += (upwardSpeed + boost) * Time.deltaTime * Vector3.up;
        }


        public void Switch() {
            direction *= -1;
        }

        public void Boost() {
            IEnumerator UpwardSpeedBoostCoroutine() {
                boost = upwardSpeedBoostStrength;

                var elapsed = 0f;
                while (elapsed < upwardSpeedBoostTime) {
                    boost = upwardSpeedBoostStrength * (1 - elapsed / upwardSpeedBoostTime);

                    elapsed += Time.deltaTime;
                    yield return null;
                }

                boost = 0f;
            }

            IEnumerator SwingBoostCoroutine() {
                swingBoost = swingBoostStrength;

                var elapsed = 0f;
                while (elapsed < swingBoostTime) {
                    swingBoost = swingBoostStrength * (1 - elapsed / swingBoostTime);

                    elapsed += Time.deltaTime;
                    yield return null;
                }

                swingBoost = 0f;
            }

            if (currentUpwardSpeedBoostCoroutine != null) StopCoroutine(currentUpwardSpeedBoostCoroutine);
            if (currentSwingBoostCoroutine != null) StopCoroutine(currentSwingBoostCoroutine);

            currentUpwardSpeedBoostCoroutine = UpwardSpeedBoostCoroutine();
            currentSwingBoostCoroutine = SwingBoostCoroutine();

            StartCoroutine(currentUpwardSpeedBoostCoroutine);
            StartCoroutine(currentSwingBoostCoroutine);
        }

        void OnTriggerEnter2D(Collider2D other) {
            if (other.CompareTag("Enemy")) OnCollided();
        }

        public void ResetState() {
            transform.position = Vector3.zero;

            if (currentSwingBoostCoroutine != null) {
                StopCoroutine(currentSwingBoostCoroutine);
                currentSwingBoostCoroutine = null;
            }

            if (currentUpwardSpeedBoostCoroutine != null) {
                StopCoroutine(currentUpwardSpeedBoostCoroutine);
                currentSwingBoostCoroutine = null;
            }

            t = 0;

            direction = 1;
        }
    }
}