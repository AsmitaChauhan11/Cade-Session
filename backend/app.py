# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from process_utils import process_training_files
# import os

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         files = request.files
#         form = request.form

#         attendance_files = request.files.getlist('attendance')
#         qna_files = request.files.getlist('qna')
#         transcript_files = request.files.getlist('transcript')
#         feedback_files = request.files.getlist('feedback')

#         repository_link = form.get('repository_link')
#         sharepoint_link = form.get('sharepoint_link')
#         training_title = form.get('training_title')

#         result = process_training_files(attendance_files, qna_files, transcript_files, feedback_files,
#                                         training_title, repository_link, sharepoint_link)

#         return send_file(result['eml_path'], as_attachment=True)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from process_utils import process_training_files
# import os
# import uuid

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         attendance_files = request.files.getlist('attendance')
#         qna_files = request.files.getlist('qna')
#         transcript_files = request.files.getlist('transcript')
#         feedback_files = request.files.getlist('feedback')

#         repository_link = request.form.get('repository_link')
#         sharepoint_link = request.form.get('sharepoint_link')
#         training_title = request.form.get('training_title')

#         # Generate unique output
#         unique_filename = f"Session_{uuid.uuid4().hex}.eml"

#         result = process_training_files(
#             attendance_files, qna_files, transcript_files, feedback_files,
#             training_title, repository_link, sharepoint_link,
#             output_filename=unique_filename  # Pass to your function
#         )

#         return send_file(result['eml_path'], as_attachment=True, mimetype='message/rfc822')

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from process_utils import process_training_files
# import os

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         # Get uploaded files and form fields
#         attendance_files = request.files.getlist('attendance')
#         qna_files = request.files.getlist('qna')
#         transcript_files = request.files.getlist('transcript')
#         feedback_files = request.files.getlist('feedback')

#         repository_link = request.form.get('repository_link')
#         sharepoint_link = request.form.get('sharepoint_link')
#         training_title = request.form.get('training_title')

#         # Process files and generate email
#         result = process_training_files(
#             attendance_files,
#             qna_files,
#             transcript_files,
#             feedback_files,
#             training_title,
#             repository_link,
#             sharepoint_link
#         )

#         return send_file(result['eml_path'], as_attachment=True)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from process_utils import process_training_files  # Your main processor function
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process():
    try:
        # Save uploaded files to disk
        def save_files(files, subfolder):
            paths = []
            for f in files:
                save_path = os.path.join(UPLOAD_FOLDER, subfolder, f.filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                f.save(save_path)
                paths.append(save_path)
            return paths

        attendance_paths = save_files(request.files.getlist('attendance'), 'attendance')
        qna_paths = save_files(request.files.getlist('qna'), 'qna')
        transcript_paths = save_files(request.files.getlist('transcript'), 'transcript')
        feedback_paths = save_files(request.files.getlist('feedback'), 'feedback')

        training_title = request.form.get('training_title')
        repository_link = request.form.get('repository_link')
        sharepoint_link = request.form.get('sharepoint_link')

        # Unique output filename
        session_id = uuid.uuid4().hex

        result = process_training_files(
            attendance_paths,
            qna_paths,
            transcript_paths,
            feedback_paths,
            training_title,
            repository_link,
            sharepoint_link,
            output_dir=OUTPUT_FOLDER,
            session_id=session_id
        )

        return jsonify({
            "success": True,
            "files": {
                "qa_docx": f"/download/{os.path.basename(result['qa_docx'])}",
                "open_docx": f"/download/{os.path.basename(result['open_docx'])}",
                "eml_path": f"/download/{os.path.basename(result['eml_path'])}"
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
