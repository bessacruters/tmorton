CKEDITOR.replace('editor1', {

      toolbar: [
         { name: 'clipboard', items: [ 'Undo', 'Redo' ] },
         { name: 'styles', items: [ 'Styles', 'Format' ] },
         { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Strike', '-', 'RemoveFormat' ] },
         { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote' ] },
         { name: 'links', items: [ 'Link', 'Unlink' ] },
         { name: 'insert', items: [ 'Image', 'Embed', 'Table' ] },
         { name: 'tools', items: [ 'Maximize' ] },
         { name: 'editing', items: [ 'Scayt' ] },
         { name: 'document', items: [ 'Source' ] }
       ],


       // Enabling extra plugins, available in the standard-all preset: https://ckeditor.com/cke4/presets-all
 extraPlugins: 'embed,image2,uploadimage,uploadfile,sourcearea',
          filebrowserUploadUrl: 'ckeditor/ck_upload.php',
         filebrowserUploadMethod: 'form',

      height: 800,

      // Load the default contents.css file plus customizations for this sample.
      contentsCss: [
        'http://cdn.ckeditor.com/4.15.0/full-all/contents.css',
        'https://ckeditor.com/docs/vendors/4.15.0/ckeditor/assets/css/widgetstyles.css'
      ],
      // Setup content provider. See https://ckeditor.com/docs/ckeditor4/latest/features/media_embed
      embed_provider: '//ckeditor.iframe.ly/api/oembed?url={url}&callback={callback}',

      // Configure the Enhanced Image plugin to use classes instead of styles and to disable the
      // resizer (because image size is controlled by widget styles or the image takes maximum
      // 100% of the editor width).
      image2_alignClasses: ['image-align-left', 'image-align-center', 'image-align-right'],
      image2_disableResizer: true
    });
