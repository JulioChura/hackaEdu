<template>
  <div class="flex items-center gap-4 mt-6 text-xs sm:text-sm text-slate-500 font-medium">
    <div class="flex -space-x-2">
      <div 
        v-for="avatar in avatars" 
        :key="avatar.id"
        class="w-7 h-7 sm:w-8 sm:h-8 rounded-full border-2 border-white bg-gray-200 bg-cover"
        :style="{ backgroundImage: `url(${avatar.url})` }"
      ></div>
    </div>
    <p class="text-xs sm:text-sm">Trusted by 10,000+ learners</p>
  </div>
</template>

<script setup>
const avatars = [
  { id: 1, url: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBht9Tz9hedllQYDoogI0TMTpwg0Z9oVgupZMoKVavg6Vdns8Gz8hwx7uWVpzGzNl656m9kI0bKyRpn6Ze5SaIyLdD549Kkt0peDTbx2qD5uHXVCyvmda5Z3yVfrJVMqq18n5jviv-tgQ2ZDN6ZUWChIaGMqhLH3WJip65loxbDmJcvhlxwm_CAbSGOeyVyUVVCQQx_lQFQP-d8wZDti8CQSHI3dOSDPlrG642tk6HhoJgWH9oHzyP_l7cweVyObLdEIAuyXZ5OT-zQ' },
  { id: 2, url: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC0p3v_GMPSZlOIBm1k-2hH0e8DccTTTXMS8e9O5CGM_8Ft71GTNRyiQCysgOa0nqpDsPm-ajNZJU1-NGkTXalAKdDnjlPI9um0Lil52jcHIf-YvLxWf_LTE4fNUL_oM5a_iBxBniQ0sTuo85kU4ZabeU6Wwkhjl_gBW8A89bcetyJzsH9lisZjZBJWoYBpkWCBXHaTLai3OHChriAAykrNyps8dRizTQS_qS0SbpGk32FE5BGsLk987tc81dXBFtLaRac2SUCZMcnw' },
  { id: 3, url: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAHcZrY6rkSST7LiEh4BmrgS-9_iGeimX1b23UlAI6kAyFtqmGupD-h50hC_-wZxiuJuyB5Fj8kKVJmxLB3-wk6_eBEVT6zVRr9eumX6wcfanxnXvyZ8UXcEUmys7dxBBw9_LkUHOieeFTxhesTx2xa7KsKprzDbaMVHk08XlD0kyj-qmKuqeIo_Kj7g_vy_fBTwQafbT3DmZCr7yr1f4jRqjqzpq1lc15OAZ1bougbrA68JT9O8QiX9febCAaE_yXaSVl36KonbskB' },
]
</script>
