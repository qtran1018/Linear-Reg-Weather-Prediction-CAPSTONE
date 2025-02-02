import linear_model_maker
import joblib

def export_model():
    model = linear_model_maker.make_model()
    joblib.dump(model,'testdump.pkl')
export_model()