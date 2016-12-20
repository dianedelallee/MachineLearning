class HelperHttp(object):

    def content_type(header, mimeType):
        return len(header.strip()) == 0 or \
            any(value.strip() == mimeType
                for value
                in header.split(';'))