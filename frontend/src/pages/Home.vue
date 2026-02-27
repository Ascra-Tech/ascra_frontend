<template>
  <div>
    <!-- Navigation -->
    <Navigation />
    
    <!-- Hero Section -->
    <HeroSection />
    
    <!-- Services Section -->
    <ServicesSection id="services" />
    
    <!-- Portfolio Section -->
    <PortfolioSection id="portfolio" />
    
    <!-- About Section -->
    <AboutSection id="about" />
    
    <!-- Contact Section -->
    <ContactSection id="contact" />
    
    <!-- Footer -->
    <FooterSection />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navigation from '../components/Navigation.vue'
import HeroSection from '../components/HeroSection.vue'
import ServicesSection from '../components/ServicesSection.vue'
import PortfolioSection from '../components/PortfolioSection.vue'
import AboutSection from '../components/AboutSection.vue'
import ContactSection from '../components/ContactSection.vue'
import FooterSection from '../components/FooterSection.vue'

// Handle hash-based navigation
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  // Handle hash navigation when coming from dashboard
  if (window.location.hash) {
    const sectionId = window.location.hash.substring(1)
    setTimeout(() => scrollToSection(sectionId), 100)
  }
})
</script>
