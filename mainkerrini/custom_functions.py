import uuid, re, os, magic, shutil
from kerrini.settings import STATIC_URL, PIC
from mainkerrini.models import Category, Playlist


def handle_upload_picture(folder, uploaded_filename, file_content):
    # create the folder if it doesn't exist.
    try:
        os.makedirs(os.path.join(PIC, folder))
    except:
        pass
    # save the uploaded file inside that folder.
    db_path = folder + '/' + uploaded_filename
    full_filename = os.path.join(PIC, folder, uploaded_filename)
    fout = open(full_filename, 'wb+')
    try:
        for chunk in file_content.chunks():
            fout.write(chunk)
            fout.close()
    except:
        pass
    return db_path


def handle_uploaded_file(f):
    temp_path = os.path.join(PIC, "temp", str(uuid.uuid1()))
    with open(temp_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    filetype = magic.from_file(temp_path, mime=True).decode()
    extension = filetype.split('/')
    extension = extension[1]
    file_name = str(uuid.uuid1())
    final_path = os.path.join(PIC, "videos/" + extension, file_name+ "." + extension)

    shutil.move(temp_path, final_path)
    final_path = "videos/" + extension + '/' + file_name + "." + extension
    return extension, final_path


def check_file_header(file):
    f = magic.Magic(mime=True)
    vid_type = f.from_buffer(file.read()).decode('utf-8')
    return vid_type


def get_categories():
    cat = Category.objects.all()
    cat_tuple = ()
    for c in cat:
        cat_tuple = ((c.category_name, c.category_name),) + cat_tuple
    return cat_tuple


def get_user_playlists(request):
    user = request.session['user_id']
    user_playlists = Playlist.objects.filter(user_id=user)
    return user_playlists
