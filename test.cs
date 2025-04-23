// Root myDeserializedClass = JsonConvert.DeserializeObject<Root>(myJsonResponse);
    public class External
    {
        public string href { get; set; }
        public string text { get; set; }
        public string title { get; set; }
        public string base_domain { get; set; }
    }

    public class Image
    {
        public string src { get; set; }
        public string data { get; set; }
        public string alt { get; set; }
        public string desc { get; set; }
        public int score { get; set; }
        public string type { get; set; }
        public int group_id { get; set; }
        public string format { get; set; }
        public object width { get; set; }
    }

    public class Internal
    {
        public string href { get; set; }
        public string text { get; set; }
        public string title { get; set; }
        public string base_domain { get; set; }
    }

    public class Links
    {
        public List<Internal> @internal { get; set; }
        public List<External> external { get; set; }
    }

    public class Markdown
    {
        public string raw_markdown { get; set; }
        public string markdown_with_citations { get; set; }
        public string references_markdown { get; set; }
        public string fit_markdown { get; set; }
        public string fit_html { get; set; }
    }

    public class Media
    {
        public List<Image> images { get; set; }
        public List<object> videos { get; set; }
        public List<object> audios { get; set; }
        public List<object> tables { get; set; }
    }

    public class Metadata
    {
        public string title { get; set; }
        public string description { get; set; }
        public string keywords { get; set; }
        public string author { get; set; }

        [JsonProperty("og:url")]
        public string ogurl { get; set; }

        [JsonProperty("og:type")]
        public string ogtype { get; set; }

        [JsonProperty("og:title")]
        public string ogtitle { get; set; }

        [JsonProperty("og:description")]
        public string ogdescription { get; set; }

        [JsonProperty("og:image")]
        public string ogimage { get; set; }

        [JsonProperty("twitter:card")]
        public string twittercard { get; set; }

        [JsonProperty("twitter:title")]
        public string twittertitle { get; set; }

        [JsonProperty("twitter:description")]
        public string twitterdescription { get; set; }

        [JsonProperty("twitter:image")]
        public string twitterimage { get; set; }

        [JsonProperty("twitter:image:alt")]
        public string twitterimagealt { get; set; }
    }

    public class ResponseHeaders
    {
        [JsonProperty("cache-control")]
        public string cachecontrol { get; set; }

        [JsonProperty("content-encoding")]
        public string contentencoding { get; set; }

        [JsonProperty("content-type")]
        public string contenttype { get; set; }
        public string date { get; set; }
        public string etag { get; set; }
        public string expires { get; set; }

        [JsonProperty("last-modified")]
        public string lastmodified { get; set; }
        public string p3p { get; set; }
        public string pragma { get; set; }
        public string server { get; set; }
        public string vary { get; set; }

        [JsonProperty("x-content-powered-by")]
        public string xcontentpoweredby { get; set; }

        [JsonProperty("x-logged-in")]
        public string xloggedin { get; set; }
    }

    public class Result
    {
        public string url { get; set; }
        public string html { get; set; }
        public bool success { get; set; }
        public string cleaned_html { get; set; }
        public Media media { get; set; }
        public Links links { get; set; }
        public object downloaded_files { get; set; }
        public object js_execution_result { get; set; }
        public object screenshot { get; set; }
        public object pdf { get; set; }
        public object mhtml { get; set; }
        public object extracted_content { get; set; }
        public Metadata metadata { get; set; }
        public string error_message { get; set; }
        public object session_id { get; set; }
        public ResponseHeaders response_headers { get; set; }
        public int status_code { get; set; }
        public object ssl_certificate { get; set; }
        public object dispatch_result { get; set; }
        public string redirected_url { get; set; }
        public object network_requests { get; set; }
        public object console_messages { get; set; }
        public Markdown markdown { get; set; }
    }

    public class Root
    {
        public bool success { get; set; }
        public List<Result> results { get; set; }
        public double server_processing_time_s { get; set; }
        public double server_memory_delta_mb { get; set; }
        public double server_peak_memory_mb { get; set; }
    }

