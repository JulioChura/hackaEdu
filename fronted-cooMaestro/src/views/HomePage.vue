<template>
  <div class="bg-background-light min-h-screen">
    <TheNavbar />
    
    <main class="pt-16 sm:pt-20">
      <HeroHome />
      <CefrLevelsHome />
      <HowItWorksHome />
      <CtaHome />
    </main>
    
    <TheFooter />
  </div>
</template>

<script setup>
import TheNavbar from '../components/layout/TheNavbar.vue'
import TheFooter from '../components/layout/TheFooter.vue'
import HeroHome from '../components/home/HeroHome.vue'
import CefrLevelsHome from '../components/home/CefrLevelsHome.vue'
import HowItWorksHome from '../components/home/HowItWorksHome.vue'
import CtaHome from '../components/home/CtaHome.vue'



</script>
