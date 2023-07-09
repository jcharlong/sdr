"""
A module for discrete-time loop filters.
"""
import numpy as np

from ._iir_filter import IIR


class LoopFilter:
    r"""
    Implements a 2nd order, proportional-plus-integrator (PPI) loop filter.

    Notes:
        .. code-block:: text
            :caption: Proportional-Plus-Integral Loop Filter Block Diagram

                       +----+
                   +-->| K1 |-------------------+
                   |   +----+                   |
            x[n] --+                            @--> y[n]
                   |   +----+                   |
                   +-->| K2 |--@-------------+--+
                       +----+  ^             |
                               |  +------+   |
                               +--| z^-1 |<--+
                                  +------+

            x[n] = Input signal
            y[n] = Output signal
            K1 = Proportional gain
            K2 = Integral gain
            z^-1 = Unit delay
            @ = Adder

        The transfer function of the loop filter is

        $$H(z) = K_1 + K_2 \frac{ 1 }{ 1 - z^{-1}} = \frac{(K_1 + K_2) - K_1 z^{-1}}{1 - z^{-1}} .$$

        The second-order proportional-plus-integrator loop filter can track a constant phase error
        and/or frequency error to zero. It cannot, however, track an constant chirp (frequency ramp)
        to zero.

    References:
        - M. Rice, Digital Communications: A Discrete-Time Approach, Appendix C: Phase Locked Loops.

    Group:
        pll
    """

    def __init__(self, noise_bandwidth: float, damping_factor: float, K0: float = 1.0, Kp: float = 1.0):
        """
        Creates a 2nd order, proportional-plus-integrator (PPI) loop filter.

        Arguments:
            noise_bandwidth: The normalized noise bandwidth $B_n T$ of the loop filter,
                where $B_n$ is the noise bandwidth in Hz and $T$ is the sampling period in seconds.
            damping_factor: The damping factor of the loop filter. A damping factor of 1 is critically damped,
                less than 1 is underdamped, and greater than 1 is overdamped.
            K0: The NCO gain.
            Kp: The gain of the phase error detector (PED) or time error detector (TED).
        """
        BnT = noise_bandwidth
        zeta = damping_factor

        # Equation C.57, page 736
        theta_n = BnT / (zeta + 1 / (4 * zeta))

        # Equation C.58, page 737
        K1 = 4 * zeta * theta_n / (1 + 2 * zeta * theta_n + theta_n**2) / K0 / Kp
        K2 = 4 * theta_n**2 / (1 + 2 * zeta * theta_n + theta_n**2) / K0 / Kp

        b = [K1 + K2, -K1]
        a = [1, -1]

        self._BnT = BnT
        self._zeta = zeta
        self._K1 = K1
        self._K2 = K2
        self._iir = IIR(b, a, streaming=True)

        self.reset()

    def reset(self) -> None:
        """
        Resets the loop filter.
        """
        self.iir.reset()

    def filter(self, x: np.ndarray) -> np.ndarray:
        """
        Filters the input signal $x[n]$.

        Arguments:
            x: The input signal, $x[n]$.

        Returns:
            The filtered signal, $y[n]$.
        """
        return self.iir.filter(x)

    @property
    def noise_bandwidth(self) -> float:
        """
        The normalized noise bandwidth $B_n T$ of the loop filter,
        where $B_n$ is the noise bandwidth in Hz and $T$ is the sampling period in seconds.
        """
        return self._BnT

    @property
    def damping_factor(self) -> float:
        """
        The damping factor of the loop filter. A damping factor of 1 is critically damped,
        less than 1 is underdamped, and greater than 1 is overdamped.
        """
        return self._zeta

    @property
    def K1(self) -> float:
        """
        The proportional gain of the loop filter.
        """
        return self._K1

    @property
    def K2(self) -> float:
        """
        The integral gain of the loop filter.
        """
        return self._K2

    @property
    def iir(self) -> IIR:
        """
        The underlying IIR filter used to implement the loop filter.
        """
        return self._iir