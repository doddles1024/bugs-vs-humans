#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GunActor.generated.h"

UCLASS()
class MYGAME_API AGunActor : public AActor
{
    GENERATED_BODY()
    
public:    
    AGunActor();
    
    virtual void Tick(float DeltaTime) override;
    
    UFUNCTION(BlueprintCallable)
    void TryShoot();
    
protected:
    virtual void BeginPlay() override;
    
private:
    UPROPERTY(EditAnywhere, Category = "Weapon")
    float CooldownTime = 0.5f;
    
    bool bCanShoot = true;
    
    FTimerHandle CooldownTimerHandle;
    
    void Shoot();
    void ResetCooldown();
};
