def laporan():
    form = SQLFORM.factory(
        Field('laporan','text')
        )
    if form.process(dbio=False).accepted:
        db.t_laporan_masyarakat.insert(uraian=request.vars.laporan)
    elif form.errors:
        response.flash = 'Ada kesalahan pengisian form'
    else:
        response.flash= "Silahkan isi"

    return dict(form = form)
