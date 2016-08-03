set -e # fail fast
set -x # print commands

git clone resource-gist updated-gist
clone resource-gist in directory: updated-gist

cd updated-gist
python resource-files/03_pipeline_train_keras_model_push_results/train_keras_mlp_predict.py > model_results
echo model_results 
git config --global user.email "ewayman@gmail.com"
git config --global user.name "ericwayman"

#commit model_results to repo
git add .
git commit -m "model_results"