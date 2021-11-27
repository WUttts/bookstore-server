from . import api
from flask import jsonify, request, current_app
import os, uuid
from models import DBSession, File


@api.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        uuid_file_name = "{0}{1}".format(uuid.uuid1(), file.filename)
        upload_path = os.path.join(os.path.dirname(__file__), "../static/upload_file", uuid_file_name)
        file.save(upload_path)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=500, message="file saving failed")
    try:
        file_name = file.filename
        real_name = os.path.basename(upload_path)
        file_type = real_name.split('.')[1]
        file_size = os.path.getsize(upload_path)
        url = "/static/upload_file/{0}".format(real_name)
        dbsession = DBSession()
        file_obj = File(file_name=file_name, real_name=real_name, file_type=file_type, file_size=file_size, url=url)
        dbsession.add(file_obj)
        dbsession.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=500, message="mysql error")
    print(file_obj.id)
    data = {
        "id": file_obj.id,
        "file_name": file_obj.file_name,
        "file_type": file_obj.file_type,
        "file_size": file_obj.file_size,
        "url": file_obj.url
    }
    dbsession.close()
    return jsonify(code=200, data=data)
