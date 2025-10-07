import { ref, nextTick, onBeforeUnmount } from 'vue'

export function useModal() {
  const modalElement = ref(null)
  const modalInstance = ref(null)
  const isInitialized = ref(false)

  // Khởi tạo modal
  const init = async () => {
    if (isInitialized.value) return
    
    await nextTick()
    
    if (!modalElement.value) {
      console.error('Modal element not found')
      return
    }

    // Import Bootstrap động để tránh conflict
    const { Modal } = await import('bootstrap')
    
    // Dispose modal cũ nếu có
    const existingModal = Modal.getInstance(modalElement.value)
    if (existingModal) {
      existingModal.dispose()
    }

    // Tạo modal mới
    modalInstance.value = new Modal(modalElement.value, {
      backdrop: 'static',
      keyboard: true
    })

    isInitialized.value = true
  }

  // Hiển thị modal
  const show = async () => {
    if (!isInitialized.value) {
      await init()
    }
    
    await nextTick()
    
    if (modalInstance.value) {
      modalInstance.value.show()
    }
  }

  // Ẩn modal
  const hide = () => {
    if (modalInstance.value) {
      modalInstance.value.hide()
    }
  }

  // Toggle modal
  const toggle = async () => {
    if (!isInitialized.value) {
      await show()
    } else {
      if (modalInstance.value) {
        modalInstance.value.toggle()
      }
    }
  }

  // Cleanup khi component unmount
  const cleanup = () => {
    if (modalInstance.value) {
      modalInstance.value.dispose()
      modalInstance.value = null
    }
    isInitialized.value = false
  }

  onBeforeUnmount(() => {
    cleanup()
  })

  return {
    modalElement,
    show,
    hide,
    toggle,
    init,
    cleanup
  }
}