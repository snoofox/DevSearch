let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertClose.addEventListener('click', function (e) {
    alertWrapper.style.display = 'none'
  })
}