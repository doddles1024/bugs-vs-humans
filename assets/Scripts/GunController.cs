using UnityEngine;
using System.Collections;

public class GunController : MonoBehaviour
{
    [SerializeField] private float cooldownTime = 0.5f; // Cooldown in seconds
    private bool canShoot = true;

    void Update()
    {
        if (Input.GetButtonDown("Fire1") && canShoot)
        {
            Shoot();
            StartCoroutine(CooldownRoutine());
        }
    }

    void Shoot()
    {
        // Your shooting logic here
        Debug.Log("Bang!");
        
        // Example: Instantiate bullet, play sound, etc.
        // Instantiate(bulletPrefab, firePoint.position, firePoint.rotation);
    }

    IEnumerator CooldownRoutine()
    {
        canShoot = false;
        yield return new WaitForSeconds(cooldownTime);
        canShoot = true;
    }
}
