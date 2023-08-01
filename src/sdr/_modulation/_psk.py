"""
A module containing a class for phase-shift keying (PSK) modulation.
"""
from __future__ import annotations

import numpy as np
import numpy.typing as npt
import scipy.integrate
import scipy.special
from typing_extensions import Literal

from .._data import unpack
from .._helper import export, extend_docstring
from .._probability import Q
from .._snr import ebn0_to_esn0, esn0_to_ebn0
from ._linear import _LinearModulation
from ._symbol_mapping import binary_code, gray_code


@export
class PSK(_LinearModulation):
    r"""
    Implements phase-shift keying (PSK) modulation and demodulation.

    Notes:
        Phase-shift keying (PSK) is a linear phase modulation scheme that encodes information by modulating
        the phase of a carrier sinusoid. The modulation order $M = 2^k$ is a power of 2 and indicates the number of
        phases used. The input bit stream is taken $k$ bits at a time to create decimal symbols
        $s[k] \in \{0, \dots, M-1\}$. These decimal symbols $s[k]$ are then mapped to complex symbols
        $x[k] \in \mathbb{C}$ by the equation

        $$x[k] = \exp\left(j\left(\frac{2\pi}{M}s[k] + \phi\right)\right) .$$

    Examples:
        See the :ref:`psk` example.

    Group:
        modulation-classes
    """

    def __init__(
        self,
        order: int,
        phase_offset: float = 0.0,
        symbol_labels: Literal["bin", "gray"] | npt.ArrayLike = "gray",
    ):
        r"""
        Creates a new PSK object.

        Arguments:
            order: The modulation order $M = 2^k$, where $k \ge 1$ is the bits per symbol.
            phase_offset: The phase offset $\phi$ in degrees.
            symbol_labels: The decimal symbol labels of consecutive complex symbols.

                - `"bin"`: The symbols are binary-coded. Adjacent symbols may differ by more than one bit.
                - `"gray":` The symbols are Gray-coded. Adjacent symbols only differ by one bit.
                - `npt.ArrayLike`: An $M$-length array whose indices are the default symbol labels and whose values are
                  the new symbol labels. The default symbol labels are $0$ to $M-1$ for phases starting at $1 + 0j$
                  and going counter-clockwise around the unit circle.
        """
        # Define the base PSK symbol map
        base_symbol_map = np.exp(1j * (2 * np.pi * np.arange(order) / order + np.deg2rad(phase_offset)))

        super().__init__(order, base_symbol_map, phase_offset)

        if symbol_labels == "bin":
            self._symbol_labels = binary_code(self.bps)
        elif symbol_labels == "gray":
            self._symbol_labels = gray_code(self.bps)
        else:
            if not np.array_equal(np.sort(symbol_labels), np.arange(self.order)):
                raise ValueError(f"Argument 'symbol_labels' have unique values 0 to {self.order-1}.")
            self._symbol_labels = np.asarray(symbol_labels)

        # Relabel the symbols
        self._symbol_map[self._symbol_labels] = self._symbol_map.copy()

    @extend_docstring(
        _LinearModulation.ber,
        {},
        r"""
        References:
            - Simon and Alouini, *Digital Communications over Fading Channels*,
              Chapter 8: Performance of Single-Channel Receivers.
            - John Proakis, *Digital Communications*, Chapter 4: Optimum Receivers for AWGN Channels.

        Examples:
            See the :ref:`psk` example.

            Plot theoretical BER curves for BPSK, QPSK, 8-PSK, and 16-PSK in an AWGN channel.

            .. ipython:: python

                bpsk = sdr.PSK(2); \
                qpsk = sdr.PSK(4); \
                psk8 = sdr.PSK(8); \
                psk16 = sdr.PSK(16); \
                ebn0 = np.linspace(-2, 10, 100)

                @savefig sdr_psk_ber_1.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.ber(ebn0, bpsk.ber(ebn0), label="BPSK"); \
                sdr.plot.ber(ebn0, qpsk.ber(ebn0), label="QPSK"); \
                sdr.plot.ber(ebn0, psk8.ber(ebn0), label="8-PSK"); \
                sdr.plot.ber(ebn0, psk16.ber(ebn0), label="16-PSK"); \
                plt.title("BER curves for PSK modulation in an AWGN channel"); \
                plt.tight_layout();
        """,
    )
    def ber(self, ebn0: npt.ArrayLike | None = None) -> np.ndarray:
        M = self.order
        k = self.bps
        ebn0 = np.asarray(ebn0)
        ebn0_linear = 10 ** (ebn0 / 10)

        if M in [2, 4]:
            # Equation 4.3-13 from Proakis
            Pb = Q(np.sqrt(2 * ebn0_linear))
        else:
            # Equation 8.29 from Simon and Alouini
            esn0 = ebn0_to_esn0(ebn0, k)
            esn0_linear = 10 ** (esn0 / 10)
            Pb = np.zeros_like(esn0_linear)
            for i in range(esn0_linear.size):
                for j in range(1, M):
                    # Equation 8.30 from Simon and Alouini
                    A = scipy.integrate.quad(
                        lambda theta, i, j: 1
                        / (2 * np.pi)
                        * np.exp(-esn0_linear[i] * np.sin((2 * j - 1) * np.pi / M) ** 2 / np.sin(theta) ** 2),
                        0,
                        np.pi * (1 - (2 * j - 1) / M),
                        args=(i, j),
                    )[0]
                    B = scipy.integrate.quad(
                        lambda theta, i, j: 1
                        / (2 * np.pi)
                        * np.exp(-esn0_linear[i] * np.sin((2 * j + 1) * np.pi / M) ** 2 / np.sin(theta) ** 2),
                        0,
                        np.pi * (1 - (2 * j + 1) / M),
                        args=(i, j),
                    )[0]

                    # Probability of landing in decision region for symbol j when symbol 0 was transmitted
                    Pj = A - B

                    # The number of bits that differ between symbol j and symbol 0
                    N_bits = unpack(self._symbol_labels[j] ^ self._symbol_labels[0], k).sum()

                    Pb[i] += Pj * N_bits

                # Equation 8.31 from Simon and Alouini
                Pb[i] /= k

        return Pb

    @extend_docstring(
        _LinearModulation.ser,
        {},
        r"""
        References:
            - Simon and Alouini, *Digital Communications over Fading Channels*,
              Chapter 8: Performance of Single-Channel Receivers.
            - John Proakis, *Digital Communications*, Chapter 4: Optimum Receivers for AWGN Channels.

        Examples:
            See the :ref:`psk` example.

            Plot theoretical SER curves for BPSK, QPSK, 8-PSK, and 16-PSK in an AWGN channel.

            .. ipython:: python

                bpsk = sdr.PSK(2); \
                qpsk = sdr.PSK(4); \
                psk8 = sdr.PSK(8); \
                psk16 = sdr.PSK(16); \
                esn0 = np.linspace(-2, 10, 100)

                @savefig sdr_psk_ser_1.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.ser(esn0, bpsk.ser(esn0), label="BPSK"); \
                sdr.plot.ser(esn0, qpsk.ser(esn0), label="QPSK"); \
                sdr.plot.ser(esn0, psk8.ser(esn0), label="8-PSK"); \
                sdr.plot.ser(esn0, psk16.ser(esn0), label="16-PSK"); \
                plt.title("SER curves for PSK modulation in an AWGN channel"); \
                plt.tight_layout();
        """,
    )
    def ser(self, esn0: npt.ArrayLike | None = None) -> np.ndarray:
        M = self.order
        k = self.bps
        esn0 = np.asarray(esn0)
        esn0_linear = 10 ** (esn0 / 10)
        ebn0 = esn0_to_ebn0(esn0, k)
        ebn0_linear = 10 ** (ebn0 / 10)

        if M == 2:
            # Equation 4.3-13 from Proakis
            Pe = Q(np.sqrt(2 * ebn0_linear))
        elif M == 4:
            # Equation 4.3-15 from Proakis
            Pe = 2 * Q(np.sqrt(2 * ebn0_linear)) * (1 - 1 / 2 * Q(np.sqrt(2 * ebn0_linear)))
        else:
            # Equation 8.18 from Simon and Alouini
            Pe = np.zeros_like(esn0_linear)
            for i in range(esn0_linear.size):
                Pe[i] = (
                    Q(np.sqrt(2 * esn0_linear[i]))
                    + scipy.integrate.quad(
                        lambda u: 2
                        / np.sqrt(np.pi)
                        * np.exp(-((u - np.sqrt(esn0_linear[i])) ** 2))
                        * Q(np.sqrt(2) * u * np.tan(np.pi / M)),
                        0,
                        np.inf,
                    )[0]
                )

        return Pe

    @property
    @extend_docstring(
        _LinearModulation.phase_offset,
        {},
        r"""
        Examples:
            See the :ref:`psk` example.

            Create a QPSK constellation with no phase offset.

            .. ipython:: python

                psk = sdr.PSK(4); \
                psk.phase_offset

                @savefig sdr_psk_phase_offset_1.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.symbol_map(psk.symbol_map);

            Create a QPSK constellation with 45° phase offset.

            .. ipython:: python

                psk = sdr.PSK(4, phase_offset=45); \
                psk.phase_offset

                @savefig sdr_psk_phase_offset_2.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.symbol_map(psk.symbol_map);
        """,
    )
    def phase_offset(self) -> float:
        return super().phase_offset

    @property
    @extend_docstring(
        _LinearModulation.symbol_map,
        {},
        r"""
        Examples:
            See the :ref:`psk` example.

            The default Gray-coded symbols. Adjacent symbols only differ by one bit.

            .. ipython:: python

                psk = sdr.PSK(8); \
                psk.symbol_map

                @savefig sdr_psk_symbol_map_1.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.symbol_map(psk.symbol_map, annotate="bin");

            The binary-coded symbols. Adjacent symbols may differ by more than one bit.

            .. ipython:: python

                psk = sdr.PSK(8, symbol_labels="bin"); \
                psk.symbol_map

                @savefig sdr_psk_symbol_map_2.png
                plt.figure(figsize=(8, 4)); \
                sdr.plot.symbol_map(psk.symbol_map, annotate="bin");
        """,
    )
    def symbol_map(self) -> np.ndarray:
        return super().symbol_map