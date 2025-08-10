
from flask import Blueprint, request, jsonify
from Application.business import slm_business

# Create a Blueprint for routes
main = Blueprint('slm', __name__)


@main.route('/slm-answer', methods=['POST'])
def get_slm_answer():
    try:
        data = request.get_json()
        return slm_business.get_slm_summary_llama_cpp(data['userInput'],
                                            data['modelName'],
                                            data['systemMessage'],
                                            data['temperature'],
                                            data['maxTokens'],
                                            data['topP'],
                                            data['topK']
                                            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
