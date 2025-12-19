export default {
  mounted(el) {
    el.classList.add('reveal-hidden')
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('reveal-hidden')
          entry.target.classList.add('reveal-visible')
          observer.unobserve(entry.target)
        }
      })
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" })
    observer.observe(el)
  }
}
