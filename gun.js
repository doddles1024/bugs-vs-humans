class Gun {
    constructor() {
        this.cooldownTime = 500; // 0.5 seconds in milliseconds
        this.canShoot = true;
    }
    
    tryShoot() {
        if (this.canShoot) {
            this.shoot();
            this.startCooldown();
        }
    }
    
    shoot() {
        // Your shooting logic here
        console.log("Bang!");
        
        // Example: Create bullet element, play sound, etc.
    }
    
    startCooldown() {
        this.canShoot = false;
        setTimeout(() => {
            this.canShoot = true;
        }, this.cooldownTime);
    }
}

// Usage
const gun = new Gun();
document.addEventListener('click', () => gun.tryShoot());
