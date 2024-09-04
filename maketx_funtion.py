import OpenImageIO as oiio


def mktx(filename):
    Input = oiio.ImageBuf(filename)
    config = oiio.ImageSpec()
    config.attribute("maketx:highlightcomp", 1)
    config.attribute("maketx:filtername", "lanczos3")
    config.attribute("maketx:opaque_detect", 1)
    ok = oiio.ImageBufAlgo.make_texture(oiio.MakeTxTexture, Input,
                                        "texture.exr", config)
    if not ok:
        print("error:", oiio.geterror())