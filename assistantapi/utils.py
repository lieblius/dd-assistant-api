import logging

import numpy as np


def pre_process(data):
    dtmf_tone = 0
    tone = []
    tones = np.array([[0, 0, 0, 0, 0],
                      [0, 1, 2, 3, 0],
                      [0, 4, 5, 6, 0],
                      [0, 7, 8, 9, 0],
                      [0, 0, 0, 0, 0]])
    if len(data) == 384080:
        audio = np.frombuffer(data[:-80], np.int16)
        dtmf = np.frombuffer(data[-80:], np.uint8)
        for i, j in zip(*[iter(dtmf)] * 2):
            tone.append(tones[i, j])
        tone = np.array(tone)
        if len(tone[np.nonzero(tone)]) != 0 and (tone == np.max(tone[np.nonzero(tone)])).sum() >= 10:
            dtmf_tone = np.max(tone[np.nonzero(tone)])
    else:
        logging.warning(f"Unexpected data length ({len(data)}), ignoring DTMF")
        audio = np.frombuffer(data, np.int16)

    logging.info(f"DTMF Tone: {dtmf_tone}")
    return audio, dtmf_tone
