import matplotlib.pyplot as plt
import numpy as np

import sdr


def test_rect_bin():
    """
    MATLAB:
        cpm = comm.CPMModulator( ...
            'ModulationOrder', 4, ...
            'SymbolMapping', 'Binary', ...
            'BitInput', true, ...
            'ModulationIndex', 0.5, ...
            'FrequencyPulse', 'Rectangular');
        b = logical(randi([0 2], 20, 1));
        b
        x = cpm(b);
        x
    """
    cpm = sdr.CPM(4, index=0.5, symbol_labels="bin", pulse_shape="rect", sps=8)
    b = np.array([0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1])
    s = sdr.pack(b, cpm.bps)
    x = cpm.modulate(s)
    x_truth = np.array(
        [
            1.000000000000000 + 0.000000000000000j,
            0.831469612302545 - 0.555570233019602j,
            0.382683432365090 - 0.923879532511287j,
            -0.195090322016128 - 0.980785280403230j,
            -0.707106781186547 - 0.707106781186548j,
            -0.980785280403230 - 0.195090322016129j,
            -0.923879532511287 + 0.382683432365090j,
            -0.555570233019602 + 0.831469612302545j,
            -0.000000000000000 + 1.000000000000000j,
            -0.555570233019602 + 0.831469612302545j,
            -0.923879532511287 + 0.382683432365090j,
            -0.980785280403230 - 0.195090322016129j,
            -0.707106781186547 - 0.707106781186548j,
            -0.195090322016128 - 0.980785280403230j,
            0.382683432365090 - 0.923879532511287j,
            0.831469612302545 - 0.555570233019602j,
            1.000000000000000 + 0.000000000000000j,
            0.980785280403230 + 0.195090322016128j,
            0.923879532511287 + 0.382683432365090j,
            0.831469612302545 + 0.555570233019602j,
            0.707106781186548 + 0.707106781186548j,
            0.555570233019602 + 0.831469612302545j,
            0.382683432365090 + 0.923879532511287j,
            0.195090322016128 + 0.980785280403230j,
            0.000000000000000 + 1.000000000000000j,
            -0.555570233019602 + 0.831469612302545j,
            -0.923879532511287 + 0.382683432365090j,
            -0.980785280403230 - 0.195090322016128j,
            -0.707106781186548 - 0.707106781186547j,
            -0.195090322016129 - 0.980785280403230j,
            0.382683432365090 - 0.923879532511287j,
            0.831469612302545 - 0.555570233019602j,
            1.000000000000000 - 0.000000000000000j,
            0.831469612302546 + 0.555570233019602j,
            0.382683432365090 + 0.923879532511287j,
            -0.195090322016127 + 0.980785280403231j,
            -0.707106781186547 + 0.707106781186548j,
            -0.980785280403231 + 0.195090322016128j,
            -0.923879532511287 - 0.382683432365090j,
            -0.555570233019602 - 0.831469612302545j,
            -0.000000000000000 - 1.000000000000000j,
            0.195090322016127 - 0.980785280403231j,
            0.382683432365090 - 0.923879532511287j,
            0.555570233019602 - 0.831469612302546j,
            0.707106781186547 - 0.707106781186548j,
            0.831469612302545 - 0.555570233019602j,
            0.923879532511286 - 0.382683432365091j,
            0.980785280403231 - 0.195090322016128j,
            1.000000000000000 - 0.000000000000000j,
            0.980785280403231 + 0.195090322016127j,
            0.923879532511287 + 0.382683432365090j,
            0.831469612302546 + 0.555570233019602j,
            0.707106781186547 + 0.707106781186548j,
            0.555570233019603 + 0.831469612302545j,
            0.382683432365091 + 0.923879532511286j,
            0.195090322016128 + 0.980785280403230j,
            0.000000000000001 + 1.000000000000000j,
            -0.195090322016127 + 0.980785280403231j,
            -0.382683432365090 + 0.923879532511287j,
            -0.555570233019602 + 0.831469612302546j,
            -0.707106781186546 + 0.707106781186549j,
            -0.831469612302545 + 0.555570233019603j,
            -0.923879532511286 + 0.382683432365091j,
            -0.980785280403230 + 0.195090322016128j,
            -1.000000000000000 + 0.000000000000001j,
            -0.980785280403230 + 0.195090322016128j,
            -0.923879532511286 + 0.382683432365091j,
            -0.831469612302545 + 0.555570233019603j,
            -0.707106781186546 + 0.707106781186549j,
            -0.555570233019602 + 0.831469612302546j,
            -0.382683432365090 + 0.923879532511287j,
            -0.195090322016127 + 0.980785280403231j,
            0.000000000000001 + 1.000000000000000j,
            0.195090322016128 + 0.980785280403230j,
            0.382683432365091 + 0.923879532511286j,
            0.555570233019603 + 0.831469612302545j,
            0.707106781186547 + 0.707106781186548j,
            0.831469612302546 + 0.555570233019602j,
            0.923879532511287 + 0.382683432365090j,
            0.980785280403231 + 0.195090322016127j,
        ]
    )
    # debug_plot(x, x_truth, cpm.sps)
    np.testing.assert_array_almost_equal(x, x_truth)


def test_rect_gray():
    """
    MATLAB:
        cpm = comm.CPMModulator( ...
            'ModulationOrder', 4, ...
            'SymbolMapping', 'Gray', ...
            'BitInput', true, ...
            'ModulationIndex', 0.5, ...
            'FrequencyPulse', 'Rectangular');
        b = logical(randi([0 2], 20, 1));
        b
        x = cpm(b);
        x
    """
    cpm = sdr.CPM(4, index=0.5, symbol_labels="gray", pulse_shape="rect", sps=8)
    b = np.array([1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1])
    s = sdr.pack(b, cpm.bps)
    x = cpm.modulate(s)
    x_truth = np.array(
        [
            1.000000000000000 + 0.000000000000000j,
            0.980785280403230 + 0.195090322016128j,
            0.923879532511287 + 0.382683432365090j,
            0.831469612302545 + 0.555570233019602j,
            0.707106781186548 + 0.707106781186548j,
            0.555570233019602 + 0.831469612302545j,
            0.382683432365090 + 0.923879532511287j,
            0.195090322016128 + 0.980785280403230j,
            0.000000000000000 + 1.000000000000000j,
            -0.555570233019602 + 0.831469612302545j,
            -0.923879532511287 + 0.382683432365090j,
            -0.980785280403230 - 0.195090322016128j,
            -0.707106781186548 - 0.707106781186547j,
            -0.195090322016129 - 0.980785280403230j,
            0.382683432365090 - 0.923879532511287j,
            0.831469612302545 - 0.555570233019602j,
            1.000000000000000 - 0.000000000000000j,
            0.831469612302546 + 0.555570233019602j,
            0.382683432365090 + 0.923879532511287j,
            -0.195090322016127 + 0.980785280403231j,
            -0.707106781186547 + 0.707106781186548j,
            -0.980785280403231 + 0.195090322016128j,
            -0.923879532511287 - 0.382683432365090j,
            -0.555570233019602 - 0.831469612302545j,
            -0.000000000000000 - 1.000000000000000j,
            0.195090322016127 - 0.980785280403231j,
            0.382683432365090 - 0.923879532511287j,
            0.555570233019602 - 0.831469612302546j,
            0.707106781186547 - 0.707106781186548j,
            0.831469612302545 - 0.555570233019602j,
            0.923879532511286 - 0.382683432365091j,
            0.980785280403231 - 0.195090322016128j,
            1.000000000000000 - 0.000000000000000j,
            0.980785280403231 + 0.195090322016127j,
            0.923879532511287 + 0.382683432365090j,
            0.831469612302546 + 0.555570233019602j,
            0.707106781186547 + 0.707106781186548j,
            0.555570233019603 + 0.831469612302545j,
            0.382683432365091 + 0.923879532511286j,
            0.195090322016128 + 0.980785280403230j,
            0.000000000000001 + 1.000000000000000j,
            -0.555570233019602 + 0.831469612302546j,
            -0.923879532511286 + 0.382683432365091j,
            -0.980785280403231 - 0.195090322016127j,
            -0.707106781186547 - 0.707106781186548j,
            -0.195090322016130 - 0.980785280403230j,
            0.382683432365090 - 0.923879532511287j,
            0.831469612302544 - 0.555570233019604j,
            1.000000000000000 - 0.000000000000001j,
            0.980785280403231 + 0.195090322016127j,
            0.923879532511288 + 0.382683432365088j,
            0.831469612302545 + 0.555570233019603j,
            0.707106781186547 + 0.707106781186548j,
            0.555570233019603 + 0.831469612302545j,
            0.382683432365091 + 0.923879532511286j,
            0.195090322016130 + 0.980785280403230j,
            -0.000000000000001 + 1.000000000000000j,
            -0.195090322016129 + 0.980785280403230j,
            -0.382683432365089 + 0.923879532511287j,
            -0.555570233019601 + 0.831469612302546j,
            -0.707106781186546 + 0.707106781186549j,
            -0.831469612302544 + 0.555570233019604j,
            -0.923879532511287 + 0.382683432365089j,
            -0.980785280403230 + 0.195090322016128j,
            -1.000000000000000 + 0.000000000000001j,
            -0.831469612302545 - 0.555570233019603j,
            -0.382683432365091 - 0.923879532511286j,
            0.195090322016128 - 0.980785280403230j,
            0.707106781186546 - 0.707106781186549j,
            0.980785280403230 - 0.195090322016129j,
            0.923879532511288 + 0.382683432365088j,
            0.555570233019603 + 0.831469612302545j,
            -0.000000000000001 + 1.000000000000000j,
            0.195090322016130 + 0.980785280403230j,
            0.382683432365091 + 0.923879532511286j,
            0.555570233019603 + 0.831469612302545j,
            0.707106781186548 + 0.707106781186547j,
            0.831469612302545 + 0.555570233019603j,
            0.923879532511288 + 0.382683432365088j,
            0.980785280403231 + 0.195090322016127j,
        ]
    )
    # debug_plot(x, x_truth, cpm.sps)
    np.testing.assert_array_almost_equal(x, x_truth)


# def test_half_sine_bin():
#     """
#     MATLAB:
#         cpm = comm.CPMModulator( ...
#             'ModulationOrder', 4, ...
#             'SymbolMapping', 'Binary', ...
#             'BitInput', true, ...
#             'ModulationIndex', 0.5, ...
#             'FrequencyPulse', 'Raised Cosine');
#         b = logical(randi([0 2], 20, 1));
#         b
#         x = cpm(b);
#         x
#     """
#     cpm = sdr.CPM(4, index=0.5, symbol_labels="bin", pulse_shape="sine", sps=8)
#     b = np.array([0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1])
#     s = sdr.pack(b, cpm.bps)
#     x = cpm.modulate(s)
#     x_truth = np.array(
#         [
#             1.000000000000000 + 0.000000000000000j,
#             0.998289041427985 - 0.058472128102156j,
#             0.909882339420709 - 0.414866398266114j,
#             0.328007474490157 - 0.944675127585452j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.944675127585452 + 0.328007474490156j,
#             -0.414866398266114 + 0.909882339420709j,
#             -0.058472128102157 + 0.998289041427985j,
#             -0.000000000000000 + 1.000000000000000j,
#             -0.058472128102157 + 0.998289041427985j,
#             -0.414866398266114 + 0.909882339420709j,
#             -0.944675127585452 + 0.328007474490156j,
#             -0.707106781186547 - 0.707106781186548j,
#             0.328007474490157 - 0.944675127585452j,
#             0.909882339420709 - 0.414866398266114j,
#             0.998289041427985 - 0.058472128102156j,
#             1.000000000000000 + 0.000000000000000j,
#             0.999809845283299 + 0.019500596775108j,
#             0.989850028790211 + 0.142115869993530j,
#             0.916241297153450 + 0.400626865537700j,
#             0.707106781186548 + 0.707106781186548j,
#             0.400626865537700 + 0.916241297153450j,
#             0.142115869993530 + 0.989850028790211j,
#             0.019500596775108 + 0.999809845283299j,
#             0.000000000000000 + 1.000000000000000j,
#             -0.058472128102156 + 0.998289041427985j,
#             -0.414866398266114 + 0.909882339420709j,
#             -0.944675127585452 + 0.328007474490157j,
#             -0.707106781186548 - 0.707106781186547j,
#             0.328007474490156 - 0.944675127585452j,
#             0.909882339420709 - 0.414866398266114j,
#             0.998289041427985 - 0.058472128102157j,
#             1.000000000000000 - 0.000000000000000j,
#             0.999809845283299 + 0.019500596775108j,
#             0.989850028790211 + 0.142115869993529j,
#             0.916241297153451 + 0.400626865537699j,
#             0.707106781186548 + 0.707106781186547j,
#             0.400626865537700 + 0.916241297153451j,
#             0.142115869993530 + 0.989850028790211j,
#             0.019500596775108 + 0.999809845283299j,
#             0.000000000000000 + 1.000000000000000j,
#             -0.058472128102156 + 0.998289041427985j,
#             -0.414866398266115 + 0.909882339420708j,
#             -0.944675127585452 + 0.328007474490156j,
#             -0.707106781186547 - 0.707106781186548j,
#             0.328007474490155 - 0.944675127585452j,
#             0.909882339420709 - 0.414866398266114j,
#             0.998289041427985 - 0.058472128102158j,
#             1.000000000000000 - 0.000000000000000j,
#             0.999809845283299 + 0.019500596775106j,
#             0.989850028790211 + 0.142115869993529j,
#             0.916241297153451 + 0.400626865537699j,
#             0.707106781186547 + 0.707106781186548j,
#             0.400626865537700 + 0.916241297153451j,
#             0.142115869993530 + 0.989850028790211j,
#             0.019500596775107 + 0.999809845283299j,
#             0.000000000000001 + 1.000000000000000j,
#             -0.058472128102157 + 0.998289041427985j,
#             -0.414866398266113 + 0.909882339420709j,
#             -0.944675127585452 + 0.328007474490156j,
#             -0.707106781186547 - 0.707106781186548j,
#             0.328007474490155 - 0.944675127585452j,
#             0.909882339420709 - 0.414866398266113j,
#             0.998289041427985 - 0.058472128102158j,
#             1.000000000000000 - 0.000000000000001j,
#             0.999809845283299 - 0.019500596775109j,
#             0.989850028790211 - 0.142115869993528j,
#             0.916241297153450 - 0.400626865537700j,
#             0.707106781186546 - 0.707106781186549j,
#             0.400626865537700 - 0.916241297153450j,
#             0.142115869993529 - 0.989850028790211j,
#             0.019500596775106 - 0.999809845283299j,
#             -0.000000000000002 - 1.000000000000000j,
#             -0.019500596775107 - 0.999809845283299j,
#             -0.142115869993530 - 0.989850028790211j,
#             -0.400626865537702 - 0.916241297153450j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.916241297153451 - 0.400626865537699j,
#             -0.989850028790211 - 0.142115869993529j,
#             -0.999809845283299 - 0.019500596775106j,
#         ]
#     )
#     # debug_plot(x, x_truth, cpm.sps)
#     np.testing.assert_array_almost_equal(x, x_truth)


# def test_raised_cosine_bin():
#     """
#     MATLAB:
#         cpm = comm.CPMModulator( ...
#             'ModulationOrder', 4, ...
#             'SymbolMapping', 'Binary', ...
#             'BitInput', true, ...
#             'ModulationIndex', 0.5, ...
#             'FrequencyPulse', 'Spectral Raised Cosine');
#         b = logical(randi([0 2], 20, 1));
#         b
#         x = cpm(b);
#         x
#     """
#     cpm = sdr.CPM(4, index=0.5, symbol_labels="bin", pulse_shape="rc", sps=8, alpha=0.2)
#     b = np.array([1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0])
#     s = sdr.pack(b, cpm.bps)
#     x = cpm.modulate(s)
#     x_truth = np.array(
#         [
#             1.000000000000000 + 0.000000000000000j,
#             0.998912973726272 + 0.046614063557427j,
#             0.979685973185829 + 0.200537761887719j,
#             0.895308537006461 + 0.445446544002029j,
#             0.707106781186548 + 0.707106781186547j,
#             0.445446544002029 + 0.895308537006460j,
#             0.200537761887720 + 0.979685973185829j,
#             0.046614063557428 + 0.998912973726272j,
#             0.000000000000000 + 1.000000000000000j,
#             0.046614063557427 + 0.998912973726272j,
#             0.200537761887719 + 0.979685973185829j,
#             0.445446544002029 + 0.895308537006460j,
#             0.707106781186547 + 0.707106781186548j,
#             0.895308537006460 + 0.445446544002029j,
#             0.979685973185829 + 0.200537761887719j,
#             0.998912973726272 + 0.046614063557428j,
#             1.000000000000000 + 0.000000000000000j,
#             0.998912973726272 - 0.046614063557427j,
#             0.979685973185829 - 0.200537761887719j,
#             0.895308537006461 - 0.445446544002029j,
#             0.707106781186548 - 0.707106781186547j,
#             0.445446544002029 - 0.895308537006460j,
#             0.200537761887720 - 0.979685973185829j,
#             0.046614063557428 - 0.998912973726272j,
#             0.000000000000000 - 1.000000000000000j,
#             0.139437045299365 - 0.990230937912052j,
#             0.569354465284160 - 0.822092143777684j,
#             0.982792944333645 - 0.184710661760510j,
#             0.707106781186548 + 0.707106781186547j,
#             -0.184710661760508 + 0.982792944333645j,
#             -0.822092143777683 + 0.569354465284162j,
#             -0.990230937912052 + 0.139437045299366j,
#             -1.000000000000000 + 0.000000000000000j,
#             -0.990230937912052 - 0.139437045299365j,
#             -0.822092143777684 - 0.569354465284160j,
#             -0.184710661760510 - 0.982792944333645j,
#             0.707106781186547 - 0.707106781186548j,
#             0.982792944333645 + 0.184710661760508j,
#             0.569354465284162 + 0.822092143777683j,
#             0.139437045299366 + 0.990230937912052j,
#             0.000000000000000 + 1.000000000000000j,
#             0.046614063557428 + 0.998912973726272j,
#             0.200537761887719 + 0.979685973185829j,
#             0.445446544002029 + 0.895308537006460j,
#             0.707106781186548 + 0.707106781186547j,
#             0.895308537006461 + 0.445446544002029j,
#             0.979685973185829 + 0.200537761887720j,
#             0.998912973726272 + 0.046614063557428j,
#             1.000000000000000 - 0.000000000000000j,
#             0.990230937912052 + 0.139437045299365j,
#             0.822092143777684 + 0.569354465284160j,
#             0.184710661760511 + 0.982792944333645j,
#             -0.707106781186547 + 0.707106781186548j,
#             -0.982792944333645 - 0.184710661760509j,
#             -0.569354465284161 - 0.822092143777683j,
#             -0.139437045299367 - 0.990230937912052j,
#             -0.000000000000000 - 1.000000000000000j,
#             -0.046614063557428 - 0.998912973726272j,
#             -0.200537761887720 - 0.979685973185829j,
#             -0.445446544002029 - 0.895308537006460j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.895308537006461 - 0.445446544002028j,
#             -0.979685973185829 - 0.200537761887719j,
#             -0.998912973726272 - 0.046614063557427j,
#             -1.000000000000000 + 0.000000000000000j,
#             -0.998912973726272 + 0.046614063557428j,
#             -0.979685973185829 + 0.200537761887720j,
#             -0.895308537006460 + 0.445446544002029j,
#             -0.707106781186547 + 0.707106781186548j,
#             -0.445446544002029 + 0.895308537006461j,
#             -0.200537761887719 + 0.979685973185829j,
#             -0.046614063557428 + 0.998912973726272j,
#             0.000000000000000 + 1.000000000000000j,
#             0.139437045299365 + 0.990230937912052j,
#             0.569354465284160 + 0.822092143777684j,
#             0.982792944333645 + 0.184710661760510j,
#             0.707106781186548 - 0.707106781186547j,
#             -0.184710661760509 - 0.982792944333645j,
#             -0.822092143777683 - 0.569354465284162j,
#             -0.990230937912052 - 0.139437045299366j,
#         ]
#     )
#     # debug_plot(x, x_truth, cpm.sps)
#     np.testing.assert_array_almost_equal(x, x_truth)


# def test_gaussian_bin():
#     """
#     MATLAB:
#         cpm = comm.CPMModulator( ...
#             'ModulationOrder', 4, ...
#             'SymbolMapping', 'Binary', ...
#             'BitInput', true, ...
#             'ModulationIndex', 0.5, ...
#             'FrequencyPulse', 'Gaussian');
#         b = logical(randi([0 2], 20, 1));
#         b
#         x = cpm(b);
#         x
#     """
#     cpm = sdr.CPM(4, index=0.5, symbol_labels="bin", pulse_shape="gaussian", sps=8, time_bandwidth=0.3)
#     b = np.array([0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0])
#     s = sdr.pack(b, cpm.bps)
#     x = cpm.modulate(s)
#     x_truth = np.array(
#         [
#             1.000000000000000 + 0.000000000000000j,
#             0.986827884293050 - 0.161773690016958j,
#             0.938475327977916 - 0.345346288204671j,
#             0.845417428021313 - 0.534106143381471j,
#             0.707106781186547 - 0.707106781186548j,
#             0.534106143381471 - 0.845417428021313j,
#             0.345346288204671 - 0.938475327977916j,
#             0.161773690016958 - 0.986827884293050j,
#             0.000000000000000 - 1.000000000000000j,
#             -0.161773690016958 - 0.986827884293050j,
#             -0.345346288204671 - 0.938475327977916j,
#             -0.534106143381471 - 0.845417428021313j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.845417428021313 - 0.534106143381471j,
#             -0.938475327977916 - 0.345346288204671j,
#             -0.986827884293050 - 0.161773690016957j,
#             -1.000000000000000 - 0.000000000000000j,
#             -0.883523872531453 - 0.468386129883267j,
#             -0.490769821271988 - 0.871289264554924j,
#             0.119269368401992 - 0.992861932879386j,
#             0.707106781186548 - 0.707106781186547j,
#             0.992861932879386 - 0.119269368401990j,
#             0.871289264554924 + 0.490769821271989j,
#             0.468386129883266 + 0.883523872531453j,
#             0.000000000000000 + 1.000000000000000j,
#             -0.468386129883267 + 0.883523872531453j,
#             -0.871289264554924 + 0.490769821271988j,
#             -0.992861932879386 - 0.119269368401992j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.119269368401990 - 0.992861932879386j,
#             0.490769821271989 - 0.871289264554924j,
#             0.883523872531453 - 0.468386129883267j,
#             1.000000000000000 - 0.000000000000000j,
#             0.883523872531452 - 0.468386129883268j,
#             0.490769821271988 - 0.871289264554924j,
#             -0.119269368401992 - 0.992861932879386j,
#             -0.707106781186548 - 0.707106781186547j,
#             -0.992861932879386 - 0.119269368401990j,
#             -0.871289264554924 + 0.490769821271989j,
#             -0.468386129883266 + 0.883523872531453j,
#             0.000000000000000 + 1.000000000000000j,
#             0.161773690016958 + 0.986827884293050j,
#             0.345346288204671 + 0.938475327977916j,
#             0.534106143381471 + 0.845417428021313j,
#             0.707106781186548 + 0.707106781186547j,
#             0.845417428021313 + 0.534106143381470j,
#             0.938475327977916 + 0.345346288204671j,
#             0.986827884293050 + 0.161773690016958j,
#             1.000000000000000 + 0.000000000000000j,
#             0.883523872531453 + 0.468386129883267j,
#             0.490769821271988 + 0.871289264554924j,
#             -0.119269368401992 + 0.992861932879386j,
#             -0.707106781186548 + 0.707106781186547j,
#             -0.992861932879386 + 0.119269368401991j,
#             -0.871289264554924 - 0.490769821271988j,
#             -0.468386129883266 - 0.883523872531453j,
#             -0.000000000000000 - 1.000000000000000j,
#             0.468386129883268 - 0.883523872531453j,
#             0.871289264554924 - 0.490769821271988j,
#             0.992861932879386 + 0.119269368401992j,
#             0.707106781186548 + 0.707106781186547j,
#             0.119269368401990 + 0.992861932879386j,
#             -0.490769821271988 + 0.871289264554925j,
#             -0.883523872531454 + 0.468386129883266j,
#             -1.000000000000000 + 0.000000000000000j,
#             -0.883523872531453 - 0.468386129883267j,
#             -0.490769821271988 - 0.871289264554924j,
#             0.119269368401990 - 0.992861932879386j,
#             0.707106781186547 - 0.707106781186548j,
#             0.992861932879386 - 0.119269368401991j,
#             0.871289264554925 + 0.490769821271988j,
#             0.468386129883266 + 0.883523872531454j,
#             0.000000000000001 + 1.000000000000000j,
#             0.468386129883266 + 0.883523872531454j,
#             0.871289264554925 + 0.490769821271988j,
#             0.992861932879386 - 0.119269368401991j,
#             0.707106781186547 - 0.707106781186548j,
#             0.119269368401990 - 0.992861932879386j,
#             -0.490769821271988 - 0.871289264554924j,
#             -0.883523872531454 - 0.468386129883265j,
#         ]
#     )
#     # debug_plot(x, x_truth, cpm.sps)
#     np.testing.assert_array_almost_equal(x, x_truth)


# def test_tammed_fm_bin():
#     """
#     MATLAB:
#         cpm = comm.CPMModulator( ...
#             'ModulationOrder', 4, ...
#             'SymbolMapping', 'Binary', ...
#             'BitInput', true, ...
#             'ModulationIndex', 0.5, ...
#             'FrequencyPulse', 'Tamed FM');
#         b = logical(randi([0 2], 20, 1));
#         b
#         x = cpm(b);
#         x
#     """
#     cpm = sdr.CPM(4, index=0.5, symbol_labels="bin", pulse_shape="rect", sps=8)
#     b = np.array([1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1])
#     s = sdr.pack(b, cpm.bps)
#     x = cpm.modulate(s)
#     x_truth = np.array(
#         [
#             1.000000000000000 + 0.000000000000000j,
#             0.855231086688294 + 0.518246841150007j,
#             0.429482354299775 + 0.903075250101077j,
#             -0.163354293263838 + 0.986567471018720j,
#             -0.707106781186547 + 0.707106781186549j,
#             -0.986567471018719 + 0.163354293263841j,
#             -0.903075250101078 - 0.429482354299772j,
#             -0.518246841150009 - 0.855231086688292j,
#             -0.000000000000000 - 1.000000000000000j,
#             0.180603411648653 - 0.983556001303875j,
#             0.366854592655120 - 0.930278295913565j,
#             0.546597249332146 - 0.837395633510548j,
#             0.707106781186547 - 0.707106781186548j,
#             0.837395633510547 - 0.546597249332147j,
#             0.930278295913564 - 0.366854592655122j,
#             0.983556001303874 - 0.180603411648654j,
#             1.000000000000000 - 0.000000000000000j,
#             0.855231086688293 - 0.518246841150008j,
#             0.429482354299775 - 0.903075250101077j,
#             -0.163354293263838 - 0.986567471018719j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.986567471018719 - 0.163354293263841j,
#             -0.903075250101078 + 0.429482354299773j,
#             -0.518246841150009 + 0.855231086688292j,
#             0.000000000000000 + 1.000000000000000j,
#             0.180603411648653 + 0.983556001303874j,
#             0.366854592655120 + 0.930278295913565j,
#             0.546597249332146 + 0.837395633510548j,
#             0.707106781186547 + 0.707106781186548j,
#             0.837395633510547 + 0.546597249332147j,
#             0.930278295913564 + 0.366854592655121j,
#             0.983556001303874 + 0.180603411648654j,
#             1.000000000000000 + 0.000000000000000j,
#             0.855231086688294 + 0.518246841150007j,
#             0.429482354299775 + 0.903075250101077j,
#             -0.163354293263838 + 0.986567471018720j,
#             -0.707106781186547 + 0.707106781186549j,
#             -0.986567471018719 + 0.163354293263841j,
#             -0.903075250101078 - 0.429482354299772j,
#             -0.518246841150009 - 0.855231086688292j,
#             -0.000000000000000 - 1.000000000000000j,
#             0.518246841150007 - 0.855231086688293j,
#             0.903075250101077 - 0.429482354299776j,
#             0.986567471018720 + 0.163354293263838j,
#             0.707106781186549 + 0.707106781186546j,
#             0.163354293263841 + 0.986567471018719j,
#             -0.429482354299773 + 0.903075250101078j,
#             -0.855231086688292 + 0.518246841150010j,
#             -1.000000000000000 + 0.000000000000000j,
#             -0.855231086688294 - 0.518246841150006j,
#             -0.429482354299775 - 0.903075250101077j,
#             0.163354293263837 - 0.986567471018720j,
#             0.707106781186547 - 0.707106781186548j,
#             0.986567471018719 - 0.163354293263841j,
#             0.903075250101078 + 0.429482354299773j,
#             0.518246841150010 + 0.855231086688292j,
#             0.000000000000001 + 1.000000000000000j,
#             -0.180603411648654 + 0.983556001303874j,
#             -0.366854592655121 + 0.930278295913564j,
#             -0.546597249332146 + 0.837395633510548j,
#             -0.707106781186546 + 0.707106781186549j,
#             -0.837395633510547 + 0.546597249332147j,
#             -0.930278295913564 + 0.366854592655122j,
#             -0.983556001303874 + 0.180603411648656j,
#             -1.000000000000000 + 0.000000000000001j,
#             -0.983556001303874 - 0.180603411648654j,
#             -0.930278295913565 - 0.366854592655119j,
#             -0.837395633510548 - 0.546597249332146j,
#             -0.707106781186547 - 0.707106781186548j,
#             -0.546597249332149 - 0.837395633510546j,
#             -0.366854592655122 - 0.930278295913564j,
#             -0.180603411648656 - 0.983556001303874j,
#             -0.000000000000002 - 1.000000000000000j,
#             0.518246841150008 - 0.855231086688293j,
#             0.903075250101077 - 0.429482354299775j,
#             0.986567471018720 + 0.163354293263835j,
#             0.707106781186547 + 0.707106781186548j,
#             0.163354293263842 + 0.986567471018719j,
#             -0.429482354299772 + 0.903075250101078j,
#             -0.855231086688292 + 0.518246841150010j,
#         ]
#     )
#     # debug_plot(x, x_truth, cpm.sps)
#     np.testing.assert_array_almost_equal(x, x_truth)


def debug_plot(x: np.ndarray, x_truth: np.ndarray, sps: int):
    # import matplotlib.pyplot as plt

    plt.figure()
    sdr.plot.time_domain(x.real, label="Test")
    sdr.plot.time_domain(x_truth.real, label="Truth")

    plt.figure()
    sdr.plot.phase_tree(x, sps, span=2)
    plt.title("Test")

    plt.figure()
    sdr.plot.phase_tree(x_truth, sps, span=2)
    plt.title("Truth")

    plt.show()
