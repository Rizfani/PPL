def user_session(request):
    username = request.session.get("username")
    kelas = request.session.get("kelas")

    return {
        "username": username,
        "kelas": kelas,
    }

