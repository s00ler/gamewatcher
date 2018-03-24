import pickle
import json
import pandas as pd

from ..models import KeyboardLog


class Predictor:

    with open('./application/datascience/estimator.pickle', 'rb') as f:
        estimator = pickle.load(f)

    def __init__(self, data):
        mouse = []
        keyboard = []

        for log in data:
            if isinstance(log, KeyboardLog):
                keyboard.append(log.to_dict())
            else:
                mouse.append(log.to_dict())
        self.keyboard = pd.DataFrame(keyboard)
        self.mouse = pd.DataFrame(mouse)
        self._preprocess()

    def predict(self):
        return self.estimator.predict(self.features)

    def _preprocess(self):
        self._preprocess_keyboard()
        self._preprocess_mouse()
        self.features = self.mouse.merge(self.keyboard, left_index=True, right_index=True, how='outer').fillna(0)

    def _preprocess_keyboard(self):
        all_kb = json.loads(open('./application/datascience/all_keys_kb.json', 'r').read())

        def preprocess_keyboard(keyboard):
            keyboard['skip'] = False
            keyboard = keyboard.sort_values(by='timestamp')
            processed_keyboard = []
            for i, (action_type, key_action, key, time, skip) in enumerate(zip(
                    keyboard.action_type,
                    keyboard.key_action,
                    keyboard.key,
                    keyboard.timestamp,
                    keyboard.skip)):
                if key_action == 'press' and not skip:
                    for r_i, (r_action_type, r_key_action, r_key, r_time, r_skip) in enumerate(zip(
                            keyboard.action_type[i + 1:],
                            keyboard.key_action[i + 1:],
                            keyboard.key[i + 1:],
                            keyboard.timestamp[i + 1:],
                            keyboard.skip[i + 1:])):
                        if r_key == key and r_key_action == key_action:
                            keyboard.iloc[i + r_i + 1, -1] = True
                        if r_i - i > 100:
                            break
                        elif r_key == key and r_key_action != key_action:
                            time_press = time
                            time_hold = r_time - time
                            time_transfer = time - processed_keyboard[-1][-3] if processed_keyboard != [] else 0
                            processed_keyboard.append((action_type, key, time_press, time_hold, time_transfer))
                            break
            processed_keyboard = pd.DataFrame(processed_keyboard,
                                              columns=['action_type', 'key', 'timestamp', 'h_time', 't_time']
                                              ).sort_values(by='timestamp')
            return processed_keyboard
        if self.keyboard.shape == (0, 0):
            preprocessed_keyboard = pd.DataFrame([{'action_type': None, 'key': None, 'timestamp': 0, 'h_time': 0, 't_time': 0}])
        else:
            preprocessed_keyboard = preprocess_keyboard(
                self.keyboard.rename(columns={'key_code': 'key'})).drop('action_type', axis=1)
        preprocessed_keyboard['presses'] = 1
        kb_features = preprocessed_keyboard.groupby('key').agg(
            {'h_time': 'mean', 't_time': 'mean', 'presses': 'count'})
        kb_features = pd.DataFrame(data=all_kb, columns=['key']).merge(kb_features.reset_index(), how='left')
        kb_features['id'] = 1
        self.keyboard = kb_features.set_index(['id', 'key']).unstack('key').fillna(0)

    def _preprocess_mouse(self):
        all_ms = json.loads(open('./application/datascience/all_keys_ms.json', 'r').read())

        def preprocess_mouse(mouse):
            processed_mouse = []
            for action_type, key, timestamp, next_ts in zip(mouse.action_type, mouse.key,
                                                            mouse.timestamp, mouse.timestamp[1:]):
                processed_mouse.append((action_type, key, timestamp, next_ts - timestamp))
            processed_mouse = pd.DataFrame(
                processed_mouse, columns=['action_type', 'key', 'timestamp', 't_time']).sort_values(by='timestamp')
            return processed_mouse

        if self.mouse.shape == (0, 0):
            preprocessed_mouse = pd.DataFrame([{'action_type': None, 'key': None, 'timestamp': 0, 't_time': 0}])
        else:
            preprocessed_mouse = preprocess_mouse(self.mouse)
        preprocessed_mouse['presses'] = 1

        ms_features = preprocessed_mouse.groupby('key').agg({'t_time': 'mean', 'presses': 'count'})
        ms_features = pd.DataFrame(data=all_ms, columns=['key']).merge(ms_features.reset_index(), how='left')
        ms_features['id'] = 1
        self.mouse = ms_features.set_index(['id', 'key']).unstack('key').fillna(0)


def prediction(data):
    predictor = Predictor(data)
    print('Predicted action type: ', predictor.predict())
