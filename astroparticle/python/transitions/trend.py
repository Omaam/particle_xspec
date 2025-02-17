"""Trend model.
"""
import math

import tensorflow as tf

from astroparticle.python.transitions.vector_autoregressive \
    import VectorAutoregressive


class Trend(VectorAutoregressive):
    def __init__(self, order, xspec_parameter_size,
                 noise_scale, dtype=tf.float32):
        """Build Transition Trend for special case of VAR model.
        """
        base_coefficients = _get_combination(order)[::-1] * tf.repeat(
            tf.constant([1.0, -1.0], dtype=dtype), order, axis=0)[::2]
        coefficients = tf.convert_to_tensor(
            [tf.linalg.diag(tf.repeat(base_coefficients[i],
                                      xspec_parameter_size))
             for i in range(order)],
            dtype=dtype)

        noise_scale = tf.convert_to_tensor(noise_scale, dtype=dtype)
        if noise_scale.shape == ():
            noise_scale = tf.repeat(noise_scale, xspec_parameter_size)
        transition_noise_cov = tf.linalg.diag(noise_scale**2)

        super(Trend, self).__init__(
            coefficients, transition_noise_cov, dtype)


def _get_combination(total_number):
    coefficients = [math.comb(total_number, i)
                    for i in range(total_number)]
    return coefficients
