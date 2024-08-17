class PixivDataForParsing:
    url = ''
    meta_count = 0
    link_type = ''
    job_id = ''
    target = ''

    def __init__(self, url, meta_count, link_type, job_id, target):
        self.url = url
        self.meta_count = meta_count
        self.link_type = link_type
        self.job_id = job_id
        self.target = target
