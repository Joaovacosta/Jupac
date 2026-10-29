const botaoMenu = document.querySelector('.menu-botao');
const menu = document.querySelector('#menu-principal');

if (botaoMenu && menu) {
  botaoMenu.addEventListener('click', () => {
    const aberto = menu.classList.toggle('aberto');
    botaoMenu.setAttribute('aria-expanded', String(aberto));
  });
}
