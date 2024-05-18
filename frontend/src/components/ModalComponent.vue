<!-- ModalComponent.vue -->
<template>
    <div> 
        <div v-if="isActive" 
            class="modal fade" 
            :class="{ show: isActive, 'd-block': isActive }"  
            tabindex="-1" 
            role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ title }}</h5>
                    <button type="button" 
                        class="close" 
                        data-dismiss="modal" 
                        aria-label="Close" 
                        @click="closeModal">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <slot></slot>
                </div>
                </div>
            </div>
        </div>
      <div v-if="isActive" class="modal-backdrop fade show"></div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
        isActive: Boolean,
        title: String
    },
    methods: {
      closeModal() {
        this.$emit('close');
      }
    }
  }
  </script>
  
