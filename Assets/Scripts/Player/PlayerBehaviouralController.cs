﻿using System;
using System.Collections;
using UnityEngine;

namespace Player {
    /// <summary>
    /// Responsible for player movement and executing player actions
    /// </summary>
    [RequireComponent(typeof(PlayerConfigurator))]
    public class PlayerBehaviouralController : MonoBehaviour {
        [SerializeField] private Transform rotatingPart;

        private float angle;

        [SerializeField] private float maxAngle;
        [SerializeField] private float swingSpeed;
        [SerializeField] private float upwardSpeed;

        [SerializeField] private float upwardSpeedBoostStrength;
        [SerializeField] private float upwardSpeedBoostTime;

        [SerializeField] private float swingBoostStrength;
        [SerializeField] private float swingBoostTime;


        private float t;
        private float direction = 1;
        private float boost;
        private float swingBoost;

        private IEnumerator currentUpwardSpeedBoostCoroutine;
        private IEnumerator currentSwingBoostCoroutine;

        private void Update() {
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
    }
}