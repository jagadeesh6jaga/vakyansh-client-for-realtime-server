import grpc
from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
from stub.speech_recognition_open_api_pb2 import Language, RecognitionConfig, RecognitionAudio, \
    SpeechRecognitionRequest
import wave
import config


# from grpc_interceptor import ClientCallDetails, ClientInterceptor
host = config.SERVER_IP
port = config.SERVER_PORT

# class GrpcAuth(grpc.AuthMetadataPlugin):
#     def __init__(self, key):
#         self._key = key

#     def __call__(self, context, callback):
#         callback((('rpc-auth-header', self._key),), None)


# class MetadataClientInterceptor(ClientInterceptor):
#
#     def __init__(self, key):
#         self._key = key
#
#     def intercept(
#             self,
#             method,
#             request_or_iterator,
#             call_details: grpc.ClientCallDetails,
#     ):
#         new_details = ClientCallDetails(
#             call_details.method,
#             call_details.timeout,
#             [("authorization", "Bearer " + self._key)],
#             call_details.credentials,
#             call_details.wait_for_ready,
#             call_details.compression,
#         )
#
#         return method(request_or_iterator, new_details)


def read_audio(file_name):
    with wave.open(file_name, 'rb') as f:
        return f.readframes(f.getnframes())


# def transcribe_url(stub, url, language, audio_format, transcription_format):
#     metadata = (('language', language),)
#     lang = Language(sourceLanguage=language)
#     config = RecognitionConfig(language=lang, audioFormat=audio_format,
#                                transcriptionFormat=RecognitionConfig.TranscriptionFormat(value=transcription_format))
#     audio = RecognitionAudio(audioUri=url)
#     request = SpeechRecognitionRequest(audio=[audio], config=config)

#     return stub.recognize(request, metadata=metadata)


def transcribe_audio_bytes(stub, audio_bytes, language, audio_format, transcription_format):
    metadata = (('language', language),)
    lang = Language(sourceLanguage=language)
    config = RecognitionConfig(language=lang, audioFormat=audio_format,
                               transcriptionFormat=RecognitionConfig.TranscriptionFormat(value=transcription_format))
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=[audio], config=config)

    return stub.recognize(request, metadata=metadata)


def flaskresponse(file_name,lang): 
    with grpc.insecure_channel('{}:{}'.format(host, port) ,options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = SpeechRecognizerStub(channel)
        language = lang
        audio_bytes = read_audio(file_name)
        response = transcribe_audio_bytes(stub, audio_bytes, language, 'wav', 'transcript')
        result=response.output[0].source

    return(result)




if __name__ == '__main__':
    # with open('secret/server.crt', 'rb') as f:
    #     trusted_certs = f.read()
    # create credentials
    # credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    host = config.SERVER_IP
    port = config.SERVER_PORT
    with grpc.insecure_channel('{}:{}'.format(host, port) ,options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = SpeechRecognizerStub(channel)
        language = 'hi'
        #audio_url = 'https://storage.googleapis.com/test_public_bucket/download.mp3'
        audio_bytes = read_audio()

        # response = transcribe_url(stub, audio_url, language, 'mp3', 'transcript')
        # print(response.output[0].source)

        # response = transcribe_url(stub, audio_url, language, 'mp3', 'srt')
        # print(response.output[0].source)

        response = transcribe_audio_bytes(stub, audio_bytes, language, 'wav', 'transcript')
        print(response.output[0].source)

        # response = transcribe_audio_bytes(stub, audio_bytes, language, 'wav', 'srt')
        # print(response.output[0].source)
