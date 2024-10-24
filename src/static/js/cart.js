document.addEventListener('DOMContentLoaded', function () {

    const getCookie = (name) => {
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        const cookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
    };

    const getGrandTotal = () => {
        const grandTotal = Array.from(document.querySelectorAll('.price'))
            .reduce((total, subtotal) => total + parseFloat(subtotal.textContent.replace('$', '')), 0);
        if (grandTotal === 0) {
            return 0;
        }
        const tax = parseFloat(document.querySelector('#tax').textContent.replace('$', ''));
        return grandTotal + tax;
    };

    const updateQuantity = (button, increment) => {
        const input = button.closest('.input-spinner').querySelector('.quantity-input');
        let quantity = parseInt(input.value);
        quantity = increment ? quantity + 1 : quantity - 1;
        if (quantity < 1) {
            removeCartItem(button);
        } else {
            input.value = quantity;
            updateCartItem(input.dataset.id, quantity);
        }
    };

    const updateCartItem = (itemId, quantity) => {
        const formData = new FormData();
        formData.append('quantity', quantity);

        fetch(`/cart/update_quantity/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => handleCartUpdateResponse(data, itemId))
            .catch(error => console.error('Error updating cart item:', error));
    };

    const handleCartUpdateResponse = (data, itemId) => {
        if (data.success) {
            document.querySelector(`#subtotal-${itemId}`).textContent = `$${data.sub_total}`;
            updateTotalPrices(data.total, data.tax);
        } else {
            console.error('Failed to update cart item');
        }
    };

    const updateTotalPrices = (total, tax) => {
        document.querySelector('#total-price').textContent = `$${total}`;
        document.querySelector('#grand-total').textContent = `$${getGrandTotal()}`;

        document.querySelector('#tax').textContent = `$${tax}`;
    };

    const removeCartItem = (button) => {
        const itemId = button.dataset.id;
        fetch(`/cart/remove/${itemId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => handleRemoveItemResponse(data, button))
            .catch(error => console.error('Error removing cart item:', error));
    };

    const handleRemoveItemResponse = (data, button) => {
        if (data.success) {

            button.closest('.cart-item').remove();
            updateTotalPrices(data.total, data.tax);
            toggleEmptyCartMessage();
        } else {
            console.error('Failed to remove cart item');
        }
    };

    const toggleEmptyCartMessage = () => {
        debugger
        const cartItems = document.querySelectorAll('.cart-item');
        const emptyCartMessage = document.querySelector('.empty-cart-message');
        if (cartItems.length === 0) {
            emptyCartMessage.classList.remove('d-none');
            toggleCheckoutButton();
        } else {
            emptyCartMessage.classList.add('d-none');
        }
    }

    function toggleCheckoutButton() {
        const checkoutButton = document.querySelector('#checkout-button');
        const grandTotal = getGrandTotal();
        if (grandTotal > 0) {
            checkoutButton.classList.remove('disabled');
        } else {
            checkoutButton.classList.add('disabled');
        }
    }

    document.querySelectorAll('.button-plus').forEach(button => {
        button.addEventListener('click', () => updateQuantity(button, true));
    });

    document.querySelectorAll('.button-minus').forEach(button => {
        button.addEventListener('click', () => updateQuantity(button, false));
    });

    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', () => removeCartItem(button));
    });

});
