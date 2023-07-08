import matplotlib.pyplot as plt
import numpy as np
import scipy.signal


class IIR:
    r"""
    Implements an infinite impulse response (IIR) filter.

    This class is a wrapper for the :func:`scipy.signal.lfilter` function. It supports one-time filtering
    and streamed filtering.

    Notes:
        An IIR filter is defined by its feedforward coefficients $b_i$ and feedback coefficients $a_j$.
        These coefficients define the difference equation

        .. math::
            y[n] = \frac{1}{a_0} \left( \sum_{i=0}^{M} b_i x[n-i] - \sum_{j=1}^{N} a_j y[n-j] \right).

        The transfer function of the filter is

        .. math::
            H(z) = \frac{\sum_{i=0}^{M} b_i z^{-i}}{\sum_{j=0}^{N} a_j z^{-j}} .

    Examples:
        See the :ref:`iir-filters` example.

    Group:
        filtering
    """

    def __init__(self, b: np.ndarray, a: np.ndarray, streaming: bool = False):
        """
        Creates an IIR filter with feedforward coefficients $b_i$ and feedback coefficients $a_j$.

        Arguments:
            b: Feedforward coefficients, $b_i$.
            a: Feedback coefficients, $a_j$.
            streaming: Indicates whether to use streaming mode. In streaming mode, previous inputs are
                preserved between calls to :meth:`filter()`.
        """
        self._b_taps = np.asarray(b, dtype=np.complex64)
        self._a_taps = np.asarray(a, dtype=np.complex64)
        self._streaming = streaming

        self._zi: np.ndarray  # The filter state. Will be updated in reset().
        self.reset()

        # Compute the zeros and poles of the transfer function
        self._zeros, self._poles, self._gain = scipy.signal.tf2zpk(self.b_taps, self.a_taps)

    def reset(self):
        """
        *Streaming-mode only:* Resets the filter state.
        """
        self._zi = scipy.signal.lfiltic(self.b_taps, self.a_taps, y=[], x=[])

    def filter(self, x: np.ndarray) -> np.ndarray:
        r"""
        Filters the input signal $x[n]$ with the IIR filter.

        Arguments:
            x: The input signal, $x[n]$.

        Returns:
            The filtered signal, $y[n]$.

        Examples:
            See the :ref:`iir-filters` example.
        """
        x = np.atleast_1d(x)

        if not self.streaming:
            self.reset()

        y, self._zi = scipy.signal.lfilter(self.b_taps, self.a_taps, x, zi=self._zi)

        return y

    def impulse_response(self, N: int = 100) -> np.ndarray:
        r"""
        Returns the impulse response $h[n]$ of the IIR filter.

        The impulse response $h[n]$ is the filter output when the input is an impulse $\delta[n]$.

        Arguments:
            N: The number of samples to return.

        Returns:
            The impulse response of the IIR filter, $h[n]$.
        """
        x = np.zeros(N, dtype=np.float32)
        x[0] = 1

        return self.filter(x)

    def step_response(self, N: int = 100) -> np.ndarray:
        """
        Returns the step response $s[n]$ of the IIR filter.

        The step response $s[n]$ is the filter output when the input is a unit step $u[n]$.

        Arguments:
            N: The number of samples to return.

        Returns:
            The step response of the IIR filter, $s[n]$.
        """
        x = np.ones(N, dtype=np.float32)

        return self.filter(x)

    def plot_impulse_response(self, N: int = 100):
        """
        Plots the impulse response $h[n]$ of the IIR filter.

        Arguments:
            N: The number of samples in the impulse response.
        """
        h = self.impulse_response(N)

        # plt.stem(np.arange(h.size), h.real, linefmt="b-", markerfmt="bo")
        plt.plot(np.arange(h.size), h.real, color="b", marker=".", label="Real")
        plt.plot(np.arange(h.size), h.imag, color="r", marker=".", label="Imaginary")
        plt.legend()
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.title("Impulse Response, $h[n]$")

    def plot_step_response(self, N: int = 100):
        """
        Plots the step response $s[n]$ of the IIR filter.

        Arguments:
            N: The number of samples in the step response.
        """
        u = self.step_response(N)

        # plt.stem(np.arange(u.size), u.real, linefmt="b-", markerfmt="bo")
        plt.plot(np.arange(u.size), u.real, color="b", marker=".", label="Real")
        plt.plot(np.arange(u.size), u.imag, color="r", marker=".", label="Imaginary")
        plt.legend()
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.title("Step Response, $s[n]$")

    @property
    def b_taps(self) -> np.ndarray:
        """
        Returns the feedforward filter taps, $b_i$.
        """
        return self._b_taps

    @property
    def a_taps(self) -> np.ndarray:
        """
        Returns the feedback filter taps, $a_j$.
        """
        return self._a_taps

    @property
    def streaming(self) -> bool:
        """
        Returns whether the filter is in streaming mode.

        In streaming mode, the filter state is preserved between calls to :meth:`filter()`.
        """
        return self._streaming

    @property
    def order(self) -> int:
        """
        Returns the order of the IIR filter, $N - 1$.
        """
        return self._a_taps.size - 1

    @property
    def zeros(self) -> np.ndarray:
        """
        Returns the zeros of the IIR filter.
        """
        return self._zeros

    @property
    def poles(self) -> np.ndarray:
        """
        Returns the poles of the IIR filter.
        """
        return self._poles

    @property
    def gain(self) -> float:
        """
        Returns the gain of the IIR filter.
        """
        return self._gain
