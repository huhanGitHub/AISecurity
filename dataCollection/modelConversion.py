import coremltools as ct




def pb2codeML():
    pb = r'/Users/hhuu0025/PycharmProjects/AISecurity/data/chessbot.pb'
    mlmodel = ct.convert(pb)
    mlmodel.save('chessbot.mlmodel')


if __name__ == '__main__':
    pb2codeML()