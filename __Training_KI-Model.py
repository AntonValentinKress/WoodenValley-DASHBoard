import time
import pandas as pd
from datetime import timedelta
import rystavariables as rysta
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error, accuracy_score
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe

#Dataframe Laden:
while True:
    try:
        df_ki = pd.read_csv("assets/Raw_Rysta_Data.csv", index_col=None)
        print("Extracting of Data successfull")
        break
    except:
        time.sleep(1)

df_ki[rysta.tst] = pd.to_datetime(df_ki[rysta.tst])
df_ki.set_index(rysta.tst, inplace=True)

def create_features(df):

  df = df.copy()
  df['hour'] = df.index.hour
  df['minute'] = df.index.minute
  df['dayofweek'] = df.index.dayofweek
  return df

df_ki_features = create_features(df_ki)

def add_lags(df):
  df = df.copy()
  target_map_C1 = df[rysta.mc1].to_dict()
  target_map_T6 = df[rysta.mt6].to_dict()
  target_map_L0 = df[rysta.ml0].to_dict()
  target_map_B0 = df[rysta.mb0].to_dict()
  target_map_P0 = df[rysta.mp0].to_dict()
  """
  Informationen von Messwerten vor 1 - 5 Stunden. Nicht unter 1 Stunde da dann
  keine Prognose möglich ist. Wird später der Prognosehorizont verringert
  kann hier auch angepasst werden.
  """
  #C1
  df["C1 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_C1)
  df["C1 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_C1)
  df["C1 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_C1)

  #T6
  df["T6 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_T6)
  df["T6 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_T6)
  df["T6 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_T6)

  #B0
  df["B0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_B0)
  df["B0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_B0)
  df["B0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_B0)

  #L0
  df["L0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_L0)
  df["L0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_L0)
  df["L0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_L0)

  #P0
  df["P0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_P0)
  df["P0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_P0)
  df["P0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_P0)

  return(df)

df_ki_features = add_lags(df_ki_features)

df = df_ki_features.sort_index()

from sklearn.model_selection import train_test_split

FEATURES = ["hour","minute","dayofweek",
            "C1 060 min","C1 090 min","C1 120 min",
            "T6 060 min","T6 090 min","T6 120 min",
            "B0 060 min","B0 090 min","B0 120 min",
            "L0 060 min","L0 090 min","L0 120 min",
            "P0 060 min","P0 090 min","P0 120 min"
            ]

TARGET = [rysta.mc1]

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

space = {
    #Fixe Werte
    'base_score': 700,
    'booster': "gbtree",
    'objective': "reg:squarederror",
    'eval_metric': "rmse",
    'n_estimators': 3000,
    'seed': 0,
    'learning_rate': 0.3,
    'early_stopping_rounds': 10,

    #Hyperparameter
    'max_depth': hp.quniform("max_depth", 5, 50, 1),
    'gamma': hp.uniform ('gamma', 0,100),
    'reg_alpha' : hp.quniform('reg_alpha', 0,200,1),
    'reg_lambda' : hp.uniform('reg_lambda', 0,200),
    'colsample_bytree' : hp.uniform('colsample_bytree', 0.5,1),
    'min_child_weight' : hp.quniform('min_child_weight', 0, 10, 1)
}


def objective(space):
    clf=xgb.XGBRegressor(
                    base_score = space['base_score'],
                    booster = space['booster'],
                    objective = space['objective'],
                    eval_metric = space['eval_metric'],
                    n_estimators =space['n_estimators'],
                    seed = space['seed'],
                    learning_rate = space['learning_rate'],
                    early_stopping_rounds = space['early_stopping_rounds'],

                    max_depth = int(space['max_depth']),
                    gamma = space['gamma'],
                    reg_alpha = space['reg_alpha'],
                    colsample_bytree=space['colsample_bytree'],
                    min_child_weight=int(space['min_child_weight'])
    )

    evaluation = [( X_train, y_train), ( X_test, y_test)]

    clf.fit(X_train, y_train,
            eval_set=evaluation,
            verbose=False)


    pred = clf.predict(X_test)
    mse = root_mean_squared_error(y_test, pred)
    print ("SCORE:", mse)
    return {'loss': mse, 'status': STATUS_OK }

trials = Trials()

best_hyperparams = fmin(fn = objective,
                        space = space,
                        algo = tpe.suggest,
                        max_evals = 2000,
                        trials = trials)

print("The best hyperparameters are : ","\n")
print(best_hyperparams)
type(best_hyperparams)

param = {
    'base_score': 700,
    'booster': "gbtree",
    'objective': "reg:squarederror",
    'eval_metric': "rmse",
    'n_estimators': 3000,
    'seed': 0,
    'learning_rate': 0.3,
    'early_stopping_rounds': 10,

    'max_depth': best_hyperparams['max_depth'],
    'gamma': best_hyperparams['gamma'],
    'reg_alpha' : best_hyperparams['reg_alpha'],
    'reg_lambda' : best_hyperparams['reg_lambda'],
    'colsample_bytree' : best_hyperparams['colsample_bytree'],
    'min_child_weight' : best_hyperparams['min_child_weight']
}

clf = xgb.XGBRegressor()
evaluation = [( X_train, y_train), ( X_test, y_test)]

clf.fit(X_train, y_train,
        eval_set=evaluation,
        verbose=False)

file_name = "reg.pkl"

import pickle
#Speichern des Modells
pickle.dump(clf, open(file_name, "wb"))

#Laden des Modells
clf = pickle.load(open(file_name, "rb"))

# Modell konrollieren --> MSE ausgeben
rmse = root_mean_squared_error(y_test, clf.predict(X_test))
print("RMSE: %f" % (rmse))