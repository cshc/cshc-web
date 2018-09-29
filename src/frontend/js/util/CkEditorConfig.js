const CkEditorConfig = () => ({
  skin: 'moono-lisa',
  toolbar_Basic: [['Source', '-', 'Bold', 'Italic']],
  toolbar_Full: [
    ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
    ['Link', 'Unlink', 'Anchor'],
    ['Image', 'Table', 'HorizontalRule'],
    ['TextColor', 'BGColor'],
    ['Smiley', 'SpecialChar'],
    ['Source'],
  ],
  toolbar: 'Full',
  height: 500,
  filebrowserWindowWidth: 940,
  filebrowserWindowHeight: 725,
  removePlugins: 'stylesheetparser',
  allowedContent: true,
  customConfig: `${window.STATIC_URL}js/ckeditor-custom.js`,
  filebrowserUploadUrl: '/ckeditor/upload/',
  filebrowserBrowseUrl: '/ckeditor/browse/',
  language: 'en-gb',
});

export default CkEditorConfig;
