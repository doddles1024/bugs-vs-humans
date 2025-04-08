#include "GunActor.h"

AGunActor::AGunActor()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AGunActor::BeginPlay()
{
    Super::BeginPlay();
}

void AGunActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void AGunActor::TryShoot()
{
    if (bCanShoot)
    {
        Shoot();
        bCanShoot = false;
        GetWorldTimerManager().SetTimer(CooldownTimerHandle, this, &AGunActor::ResetCooldown, CooldownTime, false);
    }
}

void AGunActor::Shoot()
{
    // Your shooting logic here
    UE_LOG(LogTemp, Display, TEXT("Bang!"));
    
    // Example: Spawn projectile, play effects, etc.
}

void AGunActor::ResetCooldown()
{
    bCanShoot = true;
}
