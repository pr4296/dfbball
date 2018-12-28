<template>
  <div class="container">
        <MakePicks></MakePicks>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import MakePicks from "@/components/MakePicks.vue";

export default {
  name: "home",
  components: {
    MakePicks
  },
  methods: {
    canChangePicks: function() {
        return store.state.picks.filter(p => p.isSeason).length == 5;
    },
  },
//   created() {
//         if (!sessionStorage.getItem('token') || (sessionStorage.getItem('token') && !this.canChangePicks())) {
//             this.$router.replace({ path: "/" });
//             this.$router.go(0);
//         }
//     }
};
</script>
