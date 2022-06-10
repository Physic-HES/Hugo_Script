function [errorCode] = PositionerCompensationNotchModeFiltersSet(socketId, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2)
%PositionerCompensationNotchModeFiltersSet :  Update notch mode filters parameters 
%
%	[errorCode] = PositionerCompensationNotchModeFiltersSet(socketId, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double NotchModeFr1
%		double NotchModeFa1
%		double NotchModeZr1
%		double NotchModeZa1
%		double NotchModeFr2
%		double NotchModeFa2
%		double NotchModeZr2
%		double NotchModeZa2
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCompensationNotchModeFiltersSet', socketId, PositionerName, NotchModeFr1, NotchModeFa1, NotchModeZr1, NotchModeZa1, NotchModeFr2, NotchModeFa2, NotchModeZr2, NotchModeZa2);
