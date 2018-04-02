(function(window) {
    var Shorten = function () {
        this.long_url = ''
        this.short_url = ''
        this.qr_code_short = true
        this.qr_code_label_show = true
        this.qr_code_label_short = true
        this.qr_code_size = 300
        this.qr_code_correct_level = 'H'
        this.set_listener()
        this.createQRCode()
    }

    Shorten.prototype.set_listener = function() {
        var document = window.document
        var self = this
        $(document).on('keypress','#url', function(event) {
            if (event.keyCode == 13) {
                var url = event.target.value
                self.urlshortener(url).then(function(data) {
                    self.long_url = data['long_url']
                    self.short_url = data['short_url']
                    var shorten_dom = $('#shorten_link')[0]
                    shorten_dom.href = self.short_url
                    shorten_dom.innerText = self.short_url
                    self.createQRCode()
                })
            }
        })
        $(document).on('click touch', '#create_button', function(event) {
            var url = $('#url')[0].value
            self.urlshortener(url).then(function(data) {
                self.long_url = data['long_url']
                self.short_url = data['short_url']
                var shorten_dom = $('#shorten_link')[0]
                shorten_dom.href = self.short_url
                shorten_dom.innerText = self.short_url

                self.createQRCode()
            })
        })
        $(document).on('change', 'input:radio[name=qrcode_shorten]:checked', function(event) {
            if (event.target.value == 'qr_urlshorten') {
                self.qr_code_short = true
            } else {
                self.qr_code_short = false
            }
            self.createQRCode()
        })
        $(document).on('change', 'input:radio[name=qrcode_label_shorten]:checked', function(event) {
            if (event.target.value == 'label_urlshorten') {
                self.qr_code_label_short = true
                self.qr_code_label_show = true
            } else if (event.target.value == 'label_n_urlshorten') {
                self.qr_code_label_short = false
                self.qr_code_label_show = true
            } else {
                self.qr_code_label_show = false
            }
            self.createQRCode()
        })
        $(document).on('change', '#qrsi', function(event) {
            self.qr_code_size = parseInt(event.target.value)
            self.createQRCode()
        })
        $(document).on('change', 'input:radio[name=correct_level]:checked', function(event) {
            self.qr_code_correct_level = event.target.value
            self.createQRCode()
        })
    }

    Shorten.prototype.urlshortener = function(url){
        return new Promise(function(resolve, reject) {
            jQuery.ajax({
                type: 'post',
                url: '/api/shorten',
                data: {
                    'url': url
                },
                dataType: 'json',
                success: (data) => {

                    resolve(data)
                }
            })
        })
    }

    Shorten.prototype.createQRCode = function() {
        var qrplace = document.createElement('div');

        var correctLevel = null;
        switch(this.qr_code_correct_level){
            case 'H': correctLevel = QRCode.CorrectLevel.H; break;
            case 'Q': correctLevel = QRCode.CorrectLevel.Q; break;
            case 'M': correctLevel = QRCode.CorrectLevel.M; break;
            case 'L': correctLevel = QRCode.CorrectLevel.L; break;
            default: correctLevel = QRCode.CorrectLevel.H;
        }
        var qrcode = new QRCode(qrplace, {
            width : this.qr_code_size,
            height : this.qr_code_size,
            correctLevel: correctLevel
        }).makeCode(this.qr_code_short ? this.short_url: this.long_url);

        document.getElementById('qrbox').width = this.qr_code_size;
        document.getElementById('qrbox').height = this.qr_code_size + 60;

        var qrimg = qrplace.getElementsByTagName('img')[0];
        var self = this;

        qrimg.onload = function () {
            var canvas = document.createElement('canvas');
            var width = self.qr_code_size;
            canvas.width = width + 30;
            canvas.height = width + 30 + 30;

            let ctx = canvas.getContext('2d');

            ctx.fillStyle = "#FFF";
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            ctx.fillStyle = "#000";
            ctx.font = "16px Verdana";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            if(self.qr_code_label_show) {
                if(self.qr_code_label_short) {
                    ctx.fillText(self.short_url, width/2, width + 20 + 15)
                } else {
                    ctx.fillText(self.long_url, width/2, width + 20 + 15)
                }
            }
            if (self.short_url !== '' && self.long_url !== '') {
                ctx.drawImage(qrimg, 15, 15);
            }

            document.getElementById('qrbox').src = canvas.toDataURL();
            document.getElementById('dlsubmit').href = canvas.toDataURL();
            document.getElementById('dlsubmit').download = self.long_url + '.png';
        }
    }

    window.shorten = new Shorten()
})(window)

